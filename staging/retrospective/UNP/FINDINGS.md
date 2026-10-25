# UNP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 835 weekly dates from 2008-01-04 to 2023-12-29. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed: January-March 2008 in 68cbbb6, April-December 2008 in 0019904, 2009 in 4f3f27e,
2010 in 3198278, 2011-2012 in 9e129f3, 2013-2014 in ee9a0c1, 2015-2016 in 798651a, 2017-2018 in 50bd487, 2019-2020 in
d349c70, 2021-2023 in 78b0995.

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

## 2015 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| legacy tier BUY (2015-07-24 to 2015-12-31) | 20 | +39% | +16% to +82% | 12 | 12 (+8pp) | +23% |
| legacy tier ACCUMULATE | 11 | +16% | +10% to +26% | 0 | 0 (-5pp) | +5% |
| legacy tier WATCHLIST | 10 | +7% | +0% to +12% | 0 | 0 (-10pp) | -9% |
| legacy tier AVOID (2015-01-09 to 2015-03-20) | 11 | -7% | -8% to -2% | 0 | 0 (-23pp) | -22% |
| class RICH | 48 | +17% | -8% to +82% | 12 | 12 (-5pp) | +6% |
| class FAIR (2015-03-27 to 2015-04-17) | 4 | +2% | +0% to +3% | 0 | 0 (-15pp) | -11% |

- **The legacy tier ranked the dates in order; the class did not.** BUY beat ACCUMULATE, which beat WATCHLIST, which
  beat AVOID. The AVOID dates (19.9-24.4x trailing EPS, the 92nd-99th percentile) lost money. The BUY dates came
  as the stock fell to $75-93 (13.1-16.1x), and 12 of the 20 cleared the hurdle. The class read RICH on 48 dates,
  whose outcomes ran from -8% to +82%.
- **The first half was the expensive entry.** The 28 dates to 2015-07-17 returned a median +3%; none cleared the
  hurdle, and they trailed SPY by a median 15pp. 36 RICH calls hit, from 2015-01-09 to 2015-10-23.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class RICH (every date) | 52 | +69% | +31% to +110% | 51 | 52 (+32pp) | +43% |
| legacy tier BUY (2016-01-08 to 2016-04-08) | 12 | +77% | +66% to +110% | 12 | 12 (+39pp) | +49% |
| legacy tier ACCUMULATE | 12 | +75% | +61% to +80% | 12 | 12 (+35pp) | +44% |
| legacy tier WATCHLIST | 17 | +65% | +54% to +81% | 17 | 17 (+31pp) | +39% |
| legacy tier AVOID (2016-09-30 to 2016-12-30) | 11 | +55% | +31% to +72% | 10 | 11 (+25pp) | +39% |

- **Every date made money and all beat SPY;** 51 of 52 cleared the hurdle, and every outcome landed in BULL or XBULL.
  The class read RICH on every date, and none of those calls hit.
- **The tier ranked the dates in order again,** on total and excess return alike: BUY (12.7-14.7x, as low as the
  8th percentile) +77%, down to AVOID (17.6-19.2x) +55%.
- **The trough entry.** The 19 dates from 2015-10-30 to 2016-03-04, BUY throughout at $70-89 (12.7-15.5x), returned
  +35% to +110% and all cleared the hurdle. The prints of those months were the weakest since 2009 (carloads -6% to
  -9%, every signal at BEAR from the Q4 2015 print).
- **The BEAR case never came.** Every 2015-2016 date's two-year low stayed at least 1.35 times its BEAR price.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class RICH = legacy tier AVOID (every date) | 52 | +60% | +38% to +75% | 52 | 52 (+36pp) | +40% |
| to 2017-10-20 (price below the BULL case) | 42 | +60% | +39% to +75% | 42 | 42 (+37pp) | +41% |
| from 2017-10-27 (price above the BULL case, Ratio B `inf`) | 10 | +53% | +38% to +58% | 10 | 10 (+30pp) | +39% |

- **Every date made money, cleared the hurdle and beat SPY** (median +36pp). 51 of 52 outcomes landed in XBULL. The
  class read RICH and the tier AVOID on every date, and none of those calls hit.
- **Why the model read RICH.** The P/E ran on trailing EPS at the 90th-100th percentile of its ten years (18.8-26.5x):
  FY15's $5.49 for two dates, then FY16's $5.07, a down year (-8%). The 2017 quarters were published as they came,
  with EPS up 10% to 24% and carloads up 2% and 5% in the first half. This is the 2010 pattern: the no-guide fallback
  anchors EPS on a weak last year.
- **The price passing the BULL case did not mark the top.** From 2017-10-27 the price was above the BULL scenario
  (the decade EPS CAGR at the 75th-percentile P/E). Those 10 dates returned less, a median +53% against +60%, and still
  cleared the hurdle by a wide margin.
- **The BEAR case never came.** Every 2017 date's two-year low stayed at least 2.07 times its BEAR price ($45-49).

## 2018 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class RICH = legacy tier AVOID (every date) | 53 | +30% | -8% to +58% | 22 | 50 (+6pp) | +18% |
| January-March | 13 | +36% | -8% to +50% | 7 | 13 (+14pp) | +27% |
| April-June | 13 | +19% | +13% to +31% | 0 | 13 (+6pp) | +17% |
| July-September | 13 | +28% | +20% to +35% | 3 | 12 (+8pp) | +12% |
| October-December | 14 | +43% | +26% to +58% | 12 | 12 (+2pp) | +20% |

- **Half the return of 2017, at the same reading.** Every date read RICH and AVOID again, at the 91st-100th percentile
  (22.0-28.5x: FY16's $5.07 to 2018-01-19, then FY17's adjusted $5.79). The median two-year return was +30%: 22 of 53 dates cleared the hurdle, 50
  beat SPY, by a median 6pp. One RICH call hit (2018-08-03: under the hurdle and behind SPY).
- **The two-year point lands in the 2020 crash.** 43 of the 53 dates had their two-year low in March 2020, and the
  deepest fall within two years was -39%. The one losing date, 2018-03-23 (-8%), ends on 2020-03-23. Judge this year
  by the m12-24 average (+18%) rather than the point return.
- **The April-June entries returned least** ($130-147, 22.5-25.4x): +13% to +31%, none cleared the hurdle.
- **EPS anchored on FY17 while the quarters ran ahead.** The 2018 quarters' EPS was up 27% to 43% ($1.68, $1.98,
  $2.15), mostly from the lower federal tax rate. The fallback kept FY17's $5.79, so the P/E read 22-28x.
- **The BEAR case never came,** even in March 2020: every 2018 date's two-year low stayed at least 2.19 times its BEAR
  price ($52).

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class RICH (every date) | 52 | +36% | +24% to +47% | 37 | 0 (-14pp) | +20% |
| legacy tier WATCHLIST (2019-08-23 to 2019-10-18, with AVOID weeks between) | 6 | +40% | +30% to +45% | 5 | 0 (-13pp) | +32% |
| legacy tier AVOID | 46 | +34% | +24% to +47% | 32 | 0 (-14pp) | +19% |
| January-September | 38 | +34% | +24% to +47% | 23 | 0 (-16pp) | +17% |
| October-December | 14 | +42% | +37% to +47% | 14 | 0 (-11pp) | +24% |

- **Right against the market, wrong on the hurdle.** Every date read RICH (19.8-27.3x trailing EPS, the 85th-100th
  percentile) and every one lagged SPY over two years, by a median 14pp. But the median return was +36%, and 37 of 52
  cleared the 15%/yr hurdle, so only 15 RICH calls hit (missed the hurdle as well).
- **Every two-year window ran through March 2020,** and every date's two-year low was set then (the deepest fall -39%).
  Even so, each low stayed at least 1.24 times the date's BEAR price ($52-92).
- **The tier ranked slightly better than the class:** the six WATCHLIST dates (the 85th-90th percentile, after the
  stock fell to $156-162) returned +40% against AVOID's +34%.

## 2020 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class CHEAP (2020-03-20) | 1 | +129% | +129% | 1 | 1 (+30pp) | +95% |
| class FAIR (2020-05-15) | 1 | +58% | +58% | 1 | 1 (+14pp) | +54% |
| class RICH | 50 | +30% | -3% to +103% | 23 | 25 (+0pp) | +25% |
| legacy tier BUY (2020-03-20 to 2020-04-03) | 3 | +103% | +94% to +129% | 3 | 3 (+20pp) | +67% |
| legacy tier ACCUMULATE | 4 | +70% | +58% to +88% | 4 | 4 (+14pp) | +56% |
| legacy tier WATCHLIST | 8 | +55% | +31% to +75% | 7 | 7 (+5pp) | +46% |
| legacy tier AVOID | 37 | +22% | -3% to +45% | 11 | 13 (-2pp) | +22% |
| October-December | 14 | +8% | -3% to +17% | 0 | 2 (-5pp) | +13% |

- **The class and the tier both ranked the year in order.** CHEAP beat FAIR, which beat RICH; BUY beat ACCUMULATE, which
  beat WATCHLIST, which beat AVOID.
- **The COVID crash was the entry.** The only CHEAP date since 2012, 2020-03-20 ($117.84, 14.1x FY19 EPS, the 14th
  percentile), returned +129%, the best of the year. The seven BUY or ACCUMULATE dates (2020-03-13 to 2020-04-17 and
  2020-05-15) all cleared the hurdle and beat SPY.
- **The late-2020 entries were the expensive ones.** From the Q2 print the class read RICH at the 91st-100th percentile;
  the October-December dates returned a median +8%, none cleared the hurdle, and 2020-10-16 ($209.85, 25.0x, the 100th
  percentile) lost 3%. 19 RICH calls hit, all from 2020-06-05 on.
- **The BEAR case never came:** every 2020 date's two-year low stayed at least 1.15 times its BEAR price ($92-101).

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class RICH | 48 | -2% | -12% to +11% | 0 | 6 (-5pp) | -6% |
| class CHEAP = legacy tier ACCUMULATE (2021-09-10 to 2021-10-01) | 4 | +8% | +6% to +11% | 0 | 4 (+8pp) | +2% |
| legacy tier WATCHLIST | 9 | +5% | -3% to +11% | 0 | 6 (+4pp) | -6% |
| legacy tier AVOID | 39 | -4% | -12% to +8% | 0 | 0 (-6pp) | -6% |

- **No date cleared the hurdle.** Two years on, the median date was down 2%; 10 of 52 beat SPY. 42 of the 48 RICH calls hit
  (24.1-30.8x trailing EPS, the 92nd-100th percentile).
- **The four CHEAP dates were a fallback artefact, and still the best of the year against SPY** (+8pp), though only +6% to
  +11% in total. They came from the Q2 2021 rebound quarter (freight revenue +29%) carried into BASE as 37%/yr, at the
  92nd-94th percentile.
- **The tier ranked the year:** ACCUMULATE +8%, WATCHLIST +5%, AVOID -4%. Most two-year lows fell in March 2023; the worst
  date, 2021-10-29 ($241, 29.5x), lost 12%.

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class CHEAP | 17 | +12% | +7% to +32% | 0 | 0 (-31pp) | +8% |
| class FAIR | 13 | +16% | +4% to +26% | 0 | 0 (-35pp) | +14% |
| class RICH | 22 | +3% | -7% to +19% | 0 | 0 (-21pp) | -12% |
| legacy tier BUY | 7 | +26% | +12% to +32% | 0 | 0 (-34pp) | +21% |
| legacy tier ACCUMULATE | 12 | +15% | +7% to +25% | 0 | 0 (-33pp) | +14% |
| legacy tier WATCHLIST | 12 | +16% | +4% to +24% | 0 | 0 (-25pp) | +10% |
| legacy tier AVOID | 21 | +2% | -7% to +13% | 0 | 0 (-21pp) | -12% |

- **Every date lagged SPY and missed the hurdle** (median +11%, -25pp). All 22 RICH calls hit; none of the CHEAP or FAIR
  calls did.
- **The ranking held in total return.** CHEAP and FAIR beat RICH; BUY (+26%) beat AVOID (+2%). The best entries were the
  October 2022 lows ($190-199, 19-20x, the 53rd-62nd percentile; 2022-10-14 +32%), the worst the RICH dates of
  January-March (up to 27.5x; 2022-03-25 -7%).
- **The CHEAP calls of April-July sat at the 74th-92nd percentile.** They rested on BASE growth of 24.5%/yr: Q1 2022's
  fuel-surcharge-inflated freight revenue (+17%) and the guided margin step. They returned +7% to +19%, against +22% to
  +32% for the CHEAP dates of 2022-09-30 to 2022-11-04.

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class CHEAP (2023-01-25 to 2023-07-07, with FAIR weeks between) | 22 | +21% | +13% to +32% | 0 | 0 (-24pp) | +19% |
| class FAIR | 5 | +15% | +11% to +18% | 0 | 0 (-37pp) | +15% |
| class RICH (from 2023-07-14) | 25 | +6% | -0% to +22% | 0 | 0 (-45pp) | +6% |
| legacy tier BUY | 29 | +20% | +13% to +32% | 0 | 0 (-25pp) | +18% |
| legacy tier ACCUMULATE | 10 | +9% | +6% to +17% | 0 | 0 (-41pp) | +9% |
| legacy tier WATCHLIST | 10 | +5% | +0% to +13% | 0 | 0 (-44pp) | +3% |
| legacy tier AVOID | 3 | +1% | -0% to +4% | 0 | 0 (-47pp) | -6% |

- **Ranked in order, and every date still lagged SPY** (median -33pp; none cleared the hurdle). CHEAP > FAIR > RICH, and
  BUY > ACCUMULATE > WATCHLIST > AVOID. All 25 RICH calls hit.
- **The CHEAP stretch was the low multiple** (16.8-18.8x FY22 EPS, the 18th-47th percentile); the best date, 2023-03-10
  ($196, 17.5x), returned +32%. From July the price rose and the class turned RICH; those dates returned +6%.
- **The first BEAR landing in the series:** 2023-04-06's two-year point fell on 2025-04-04, in the April 2025 sell-off.
  The price there ($213, +13% with dividends) was nearer the BEAR price ($155) than BASE ($273). Every 2023 date's
  two-year low stayed at least 1.20 times its BEAR price.

## Across 2008-2023: the no-guide fallbacks are the open question

UNP gave no numeric full-year guide from 2009 on, so three fallbacks did the work: the last full year's EPS stands,
BASE growth takes the latest quarter's revenue growth, and there is no margin step. They anchored on the peak in
2009, the trough in 2010, and last year's earnings while margins expanded in 2012. RICH set its line too low from
2009 to 2012, was right from mid-2013 into 2015, and read RICH through the 2015-2016 trough and the 2017-2018 rise
as well. 228 of the 650 RICH dates hit (miss the hurdle and lag SPY): 24 in 2013, 44 in 2014, 36 in 2015, one in
2018, 15 in 2019, 19 in 2020, 42 in 2021, 22 in 2022, 25 in 2023. In 2019 every RICH date lagged SPY, but most still
cleared the hurdle; from 2021 almost none did.

**CHEAP stopped paying in 2021-2023.** All 46 CHEAP dates of 2008-2020 cleared the hurdle; none of the 43 of 2021-2023
did, and only the four of 2021 beat SPY. The ranking still held (CHEAP or FAIR above RICH in 2022 and 2023), so the class
ordered the dates, but its line sat too high for a stock that lagged the market for three years. From 2021 UNP gave
numeric operating-ratio guides, and the guided margin step joined the latest-quarter revenue fallback in BASE. In 2021-2022
that fallback carried a rebound quarter and fuel-surcharge-inflated quarters, which is what put CHEAP at the 74th-94th
percentile.

**At the troughs the legacy tier ranked better than the class.** From July 2009 and through 2015-2016 the fallback
carried the trough quarters' revenue declines into BASE, so the class read RICH. The legacy tier, whose Ratio B keeps
BULL on the decade CAGR, stayed at BUY or ACCUMULATE on the cheap dates and ranked the dates in order: 2009 BUY +112%
against ACCUMULATE +55%; 2015 BUY +39% down to AVOID -7%; 2016 BUY +77% down to AVOID +55%; 2020 BUY +103% down to
AVOID +22%. The class ranked 2020 too, but on one CHEAP and one FAIR date. The tier ranked 2021-2023 as well: 2021
ACCUMULATE +8% down to AVOID -4%; 2022 BUY +26% down to AVOID +2%; 2023 BUY +20% down to AVOID +1%.

**A high P/E percentile did not separate 2010 from 2014.** Both read RICH at the top of the stock's own range: in 2010
at the 99th-100th percentile on trailing FY09 EPS, with a median two-year return of +54%; in 2014 at the 90th-100th
percentile on trailing FY13 EPS, with -9%. What was visible at the time: 2010's P/E ran on a trough year (FY09 EPS
-17%), 2014's on a record year after four years of growth. 2017 fits the 2010 side (a down year, FY16 -8%: +60%);
2018 sits between (a record year, but a tax cut published in the quarters: +30%).

Candidates to test on other companies without guidance, never fitted to UNP's outcomes:
- trailing-four-quarter EPS, which is published by AS_OF and so carries no hindsight;
- a margin step from the latest quarters' published operating-ratio change;
- a cyclical BEAR from the worst two-year run rather than the worst year applied twice;
- a P/E on normalized earnings (the ten-year median or trend EPS), which would read a trough year and a record year
  differently;
- BASE growth from more than one quarter (or the decade median), so a single trough quarter does not set two years.
