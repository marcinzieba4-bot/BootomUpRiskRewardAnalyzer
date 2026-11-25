# UNH retrospective findings (hindsight)

Patterns seen in `outcome.json` for the UNH weekly dates: 731, 105 from 2008-01-04 to 2009-12-31, 209 from 2010-01-08 to 2013-12-31,
208 from 2014-01-10 to 2017-12-29 and 209 from 2018-01-05 to 2021-12-31, all UnitedHealth Group Incorporated (NYSE: UNH). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build, validation, README section and firewall result were committed and pushed (95bb426, the builder fix the firewall's first
run needed 36eb1c4, firewall result 4a203a3); the outcomes were computed on 2026-11-24. Every date has its 6-month, 1-, 2- and 3-year
horizons (the last ends 2012-12-28 for 2008-2009 and 2016-12-30 for 2010-2013). The 2010-2013 batch was decided in the session that
scored 2008-2009 (disclosed in retro/README.md, "UNH 2010-2013") and scored only after its build, validation outputs, README section and
firewall result were committed and pushed (5ed6613, 237ded5, 5fcd318, ac1542c), on 2026-11-24. The 208 dates of 2014-2017 (2014-01-10 to
2017-12-29) were built in a new session that did not open these findings or any outcome before scoring (disclosed in retro/README.md,
"UNH 2014-2017"), and scored only after its build, validation outputs, README section and firewall result were committed and pushed
(3f76218, 4a671e7, c7ba971, 96a0fd5), on 2026-11-24; their last horizon ends 2020-12-29. The 209 dates of 2018-2021 were decided in
the session that scored 2014-2017 (disclosed in retro/README.md, "UNH 2018-2021") and scored only after their build, validation
outputs, README section and firewall result were committed and pushed (7e2ea9a, b991f64, 1041443, f48751d), on 2026-11-25; their last
horizon ends 2024-12-30. Total returns include the dividends (the
annual $0.03 to the ex-date of 2010-04-01, then quarterly: $0.125 from 2010-06-03, $0.163 from 2011-06-03, $0.213 from 2012-06-13, $0.28
from 2013-06-13, $0.375 from 2014-06-12, $0.50 from 2015-06-11, $0.625 from 2016-06-15, $0.75 from 2017-06-15, $0.90 from 2018-06-15,
$1.08 from 2019-06-14, $1.25 from 2020-06-19, $1.45 from 2021-06-18, $1.65 from 2022-06-16, $1.88 from 2023-06-15, $2.10 from
2024-06-17). No split falls in any horizon, so every price is as traded.
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1%
over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within 15pp of
it either way. Every 2008-2012 date was CHEAP and BUY, so those tables test that one call against the calendar; 2013 has 29 CHEAP and
BUY dates and 24 FAIR (5 BUY, 19 ACCUMULATE); 2014-2017 has 192 RICH dates (14 WATCHLIST, 178 AVOID) and 16 FAIR (7 ACCUMULATE,
9 WATCHLIST), and RICH expects the stock to miss the hurdle and lag SPY; 2018-2021 has 180 RICH, 22 FAIR and 7 CHEAP dates (tiers
AVOID 139, WATCHLIST 50, ACCUMULATE 15, BUY 5).

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +6.9% | -43.6% to +111.7% | 16 | 36 | -1.0% | 38 |
| FY07E $3.495 (2008-01-04 to 2008-01-18) | 3 | -41.0% | -43.6% to -37.8% | 0 | 0 | -52.9% | 0 |
| FY08E $3.975 (2008-01-23 to 2008-04-18) | 13 | -25.2% | -34.0% to -2.5% | 0 | 3 | -39.3% | 3 |
| FY08E $3.575 (2008-04-23 to 2008-06-27) | 10 | -7.6% | -17.2% to +16.2% | 0 | 9 | -11.4% | 8 |
| FY08E $3 (2008-07-03 to 2008-11-28) | 22 | +36.1% | -2.4% to +111.7% | 11 | 22 | +28.6% | 22 |
| FY08E $2.965 (2008-12-05 to 2008-12-31) | 5 | +37.7% | +34.0% to +78.7% | 5 | 2 | +25.1% | 5 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | -41.0% | -43.6% to -37.8% | 0 | 0 | -52.9% | 0 |
| latest print Q4 2007 (2008-01-23 to 2008-04-18) | 13 | -25.2% | -34.0% to -2.5% | 0 | 3 | -39.3% | 3 |
| latest print Q1 2008 (2008-04-23 to 2008-07-18) | 13 | -5.8% | -17.2% to +36.1% | 1 | 12 | -9.9% | 11 |
| latest print Q2 2008 (2008-07-23 to 2008-10-10) | 12 | +17.5% | -2.4% to +99.8% | 3 | 12 | +7.9% | 12 |
| latest print Q3 2008 (2008-10-17 to 2008-12-31) | 12 | +64.0% | +34.0% to +111.7% | 12 | 9 | +39.2% | 12 |

- **CHEAP failed on 15 dates, all from 2008-01-04 to 2008-05-23, and held on the other 90.** The January 2008 entries ($54.40-56.00,
  15.6-16.0x the FY2007 guide) returned -43.6% to -37.8% over two years, the dates on the FY2008 guide of $3.975 (2008-01-23 to 2008-04-18,
  $34.40-50.35, 8.7-12.7x) -34.0% to -2.5%: 13 of these 16 lagged SPY (all but 2008-03-20, 2008-03-28 and 2008-04-04) and none cleared the
  hurdle; the other two misses are 2008-04-23 and 2008-05-23. From the Q1 2008 print the call held on 35 of 37 dates of 2008, and on
  every 2008 date from 2008-07-03 (FY08E $3.00 and $2.965, $17.15-33.01, 5.7-11.0x), which returned -2.4% to +111.7% (the 22 dates on
  FY08E $3.00: median +36.1%, every one beating SPY). Every 2008 entry sat through a 46-71% drawdown (the low close $16.30 on 2008-11-20); two years on
  the price was $28.30-37.82.
- **The guide fell faster than the price in early 2008.** FY08E went from $3.975 (January) to $3.575 (April), $3.00 (July) and $2.965
  (December), and FY2008 came in at the company's $2.95 (GAAP $2.40): the early-2008 dates were "cheap" on an EPS anchor 35% above what the year
  turned out to be. Once the anchor had been cut to where it ended, the same rules (the decade's 18.5-19.0x median, the 14x EPP floor)
  called a multiple of 6-11x, and those dates' price stood at $28.30-37.82 two years on (8.7-11.7x FY2009's $3.24). Hypothesis, not a rule: a CHEAP call on a guide that is being cut in successive releases (here three cuts in
  six months, each with a lower margin guide) is weaker than one on a guide that has stopped falling; method r2 reads each guide as it
  stands. Test it on other tickers and periods with repeated guide cuts, never fit it to UNH.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +83.5% | +45.7% to +151.5% | 52 | 46 | +53.7% | 52 |
| FY08E $2.965 (2009-01-09 to 2009-01-16) | 2 | +61.6% | +47.0% to +61.6% | 2 | 1 | +30.3% | 2 |
| FY09E $3.025 (2009-01-23 to 2009-07-17) | 26 | +106.5% | +45.7% to +151.5% | 26 | 21 | +57.6% | 26 |
| FY09E $3.075 (2009-07-22 to 2009-10-16) | 13 | +79.3% | +52.2% to +105.5% | 13 | 13 | +51.2% | 13 |
| FY09E $3.15 (2009-10-21 to 2009-12-31) | 11 | +65.0% | +51.2% to +94.2% | 11 | 11 | +54.5% | 11 |
| latest print Q3 2008 (2009-01-09 to 2009-01-16) | 2 | +61.6% | +47.0% to +61.6% | 2 | 1 | +30.3% | 2 |
| latest print Q4 2008 (2009-01-23 to 2009-04-17) | 13 | +88.5% | +45.7% to +151.5% | 13 | 8 | +48.6% | 13 |
| latest print Q1 2009 (2009-04-22 to 2009-07-17) | 13 | +106.5% | +75.4% to +125.1% | 13 | 13 | +57.6% | 13 |
| latest print Q2 2009 (2009-07-22 to 2009-10-16) | 13 | +79.3% | +52.2% to +105.5% | 13 | 13 | +51.2% | 13 |
| latest print Q3 2009 (2009-10-21 to 2009-12-31) | 11 | +65.0% | +51.2% to +94.2% | 11 | 11 | +54.5% | 11 |

- **CHEAP held on all 52 dates of 2009.** From $17.90-31.68 (5.9-10.1x FY09E) the 2009 entries returned +45.7% to +151.5% over two years
  and +78.9% to +211.0% over three, all clearing both hurdles and 46 beating SPY over two years (all 52 over three). FY2009 came in at $3.24
  (the Q4 2009 release, 2010-01-21, outside the series) against the $3.025-3.15 the models used, and two years on the price was
  $38.45-53.13.

Across the 105 dates:
- **Entry price explains most of the result.** The correlation of the entry price with the two-year total return is -0.81; the ten lowest
  entries (2008-10-10 to 2009-04-03, $17.15-21.36) returned a median +110.2%. One stock over two years mostly tests "buy lower" (retro/README.md,
  "Scoring a single stock"): judge the series by `return_to_avg_price_m12_m24_pct` (median -1.0% for 2008, +53.7% for 2009).
- **The BEAR and BASE scenarios bracketed the outcome; BULL never came.** The two-year price landed nearest the BEAR case on 46 dates
  (33 of 2008) and the BASE case on 59; never near BULL or XBULL, whose +25-39%/yr EPS paths (the 1997-2007 compounding) did not recur. The
  price went under the EPP floor within two years on every date (on most 2008-2009 dates it already was).
- **The signals added little.** The proxy composite was 1.80-2.45 on every date (premium growth at BEAR through Q2 2008, the settlement
  quarter's operating cost ratio at BEAR); the verdict came from the valuation and the EPP distance, as the BEAR- and XBULL-signal
  sensitivity runs showed before any outcome (no class moves either way).
- **Profile drift:** the kind (DURABLE, risk 2) matches today's profile, which records a later regulatory probe and Medicare Advantage
  exits (a 2026 analysis, read here only through `profile_drift`).

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +67.4% | +45.7% to +103.2% | 52 | 52 | +53.8% | 52 |
| FY09E $3.15 (2010-01-08 to 2010-01-15) | 2 | +64.5% | +59.2% to +64.5% | 2 | 2 | +42.9% | 2 |
| FY10E $3 (2010-01-22 to 2010-04-16) | 13 | +68.9% | +57.7% to +90.4% | 13 | 13 | +48.1% | 13 |
| FY10E $3.25 (2010-04-21 to 2010-07-16) | 13 | +93.6% | +84.4% to +103.2% | 13 | 13 | +70.6% | 13 |
| FY10E $3.5 (2010-07-21 to 2010-10-15) | 13 | +63.8% | +56.2% to +84.5% | 13 | 13 | +55.3% | 13 |
| FY10E $3.9 (2010-10-20 to 2010-12-31) | 11 | +53.1% | +45.7% to +59.1% | 11 | 11 | +49.6% | 11 |
| latest print Q3 2009 (2010-01-08 to 2010-01-15) | 2 | +64.5% | +59.2% to +64.5% | 2 | 2 | +42.9% | 2 |
| latest print Q4 2009 (2010-01-22 to 2010-04-16) | 13 | +68.9% | +57.7% to +90.4% | 13 | 13 | +48.1% | 13 |
| latest print Q1 2010 (2010-04-21 to 2010-07-16) | 13 | +93.6% | +84.4% to +103.2% | 13 | 13 | +70.6% | 13 |
| latest print Q2 2010 (2010-07-21 to 2010-10-15) | 13 | +63.8% | +56.2% to +84.5% | 13 | 13 | +55.3% | 13 |
| latest print Q3 2010 (2010-10-20 to 2010-12-31) | 11 | +53.1% | +45.7% to +59.1% | 11 | 11 | +49.6% | 11 |

- **CHEAP held on all 52 dates of 2010.** From $28.30-37.82 (8.7-11.5x FY10E) the entries returned +45.7% to +103.2% over two years (median
  +67.4%) against SPY's +15.7% to +38.6%, every one clearing the hurdle and beating SPY, and +62.1% to +144.4% over three (all both). The
  dates after the Q1 2010 print ($28.30-31.33, 8.7-9.6x FY10E $3.25) did best, +84.4% to +103.2%. Two years on the price was $51.00-59.51,
  and the two-year price landed nearest the BASE case on every date.
- **The guide rose all year.** FY10E went from $3.00 (the $2.90-3.10 range of November 2009) to $3.25, $3.50 and $3.90, and FY2010 came in
  at $4.10 (the Q4 2010 release, 2011-01-20): the anchor sat 5-27% under the year's outcome, the reverse of early 2008. The schedule's
  6.6%-7.1% operating margin guide, which made BASE +0.5% to +2.8% from the Q1 2010 print, compared with an outcome of 8.35%.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +40.3% | +22.9% to +73.6% | 37 | 43 | +28.7% | 48 |
| FY10E $3.9 (2011-01-07 to 2011-01-14) | 2 | +39.2% | +34.4% to +39.2% | 2 | 2 | +43.2% | 2 |
| FY11E $3.6 (2011-01-21 to 2011-04-15) | 13 | +34.5% | +22.9% to +42.8% | 9 | 13 | +29.3% | 13 |
| FY11E $4 (2011-04-21 to 2011-07-15) | 13 | +31.3% | +23.1% to +33.2% | 2 | 9 | +12.4% | 9 |
| FY11E $4.2 (2011-07-20 to 2011-10-14) | 13 | +61.9% | +41.9% to +69.3% | 13 | 12 | +30.3% | 13 |
| FY11E $4.425 (2011-10-19 to 2011-10-28) | 2 | +51.8% | +40.6% to +51.8% | 2 | 1 | +33.3% | 2 |
| FY11E $4.545 (2011-11-04 to 2011-12-30) | 9 | +54.5% | +48.4% to +73.6% | 9 | 6 | +32.3% | 9 |
| latest print Q3 2010 (2011-01-07 to 2011-01-14) | 2 | +39.2% | +34.4% to +39.2% | 2 | 2 | +43.2% | 2 |
| latest print Q4 2010 (2011-01-21 to 2011-04-15) | 13 | +34.5% | +22.9% to +42.8% | 9 | 13 | +29.3% | 13 |
| latest print Q1 2011 (2011-04-21 to 2011-07-15) | 13 | +31.3% | +23.1% to +33.2% | 2 | 9 | +12.4% | 9 |
| latest print Q2 2011 (2011-07-20 to 2011-10-14) | 13 | +61.9% | +41.9% to +69.3% | 13 | 12 | +30.3% | 13 |
| latest print Q3 2011 (2011-10-19 to 2011-12-30) | 11 | +53.3% | +40.6% to +73.6% | 11 | 7 | +32.3% | 11 |

- **CHEAP held on 48 of 52 dates of 2011.** The entries ($38.45-53.13, 9.6-13.3x FY11E) returned +22.9% to +73.6% over two years (median
  +40.3%) against SPY's +16.9% to +60.6%; 37 cleared the hurdle and 43 beat SPY. The four misses are 2011-05-06, 2011-05-20, 2011-06-10 and
  2011-06-17 ($49.41-50.12, 12.4-12.5x FY11E $4.00): +23.1% to +32.1%, just under the +32.2% hurdle and 0.5-2.1pp behind SPY. Over three
  years every 2011 date cleared both (+55.4% to +131.2%).
- **The weakest group is the one with the negative BASE.** The 13 dates after the Q1 2011 print (FY11E $4.00, $47.81-53.13, 12.0-13.3x)
  carried BASE -5.8%/yr from the margin derived from the Q1 2011 schedule (7.28% against FY10's 8.35%), and returned +23.1% to +33.2%
  (median +31.3%; 2 cleared the hurdle, 9 beat SPY), the batch's lowest; but they were also among the year's highest entries, and the class
  did not rest on BASE (the run without the FY2011 margin step moved no class before any outcome). FY11E was then raised to $4.20, $4.425
  and $4.545, and FY2011 came in at $4.73 with an operating margin of 8.31%: the derived margin guide was a point under the year's.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +53.6% | +30.7% to +95.0% | 51 | 36 | +34.1% | 51 |
| FY11E $4.545 (2012-01-06 to 2012-01-13) | 2 | +44.2% | +43.8% to +44.2% | 2 | 0 | +25.3% | 2 |
| FY12E $4.65 (2012-01-20 to 2012-04-13) | 13 | +41.5% | +34.3% to +55.3% | 13 | 10 | +23.5% | 13 |
| FY12E $4.875 (2012-04-20 to 2012-07-13) | 13 | +43.0% | +30.7% to +54.0% | 12 | 2 | +29.6% | 12 |
| FY12E $4.95 (2012-07-20 to 2012-10-12) | 13 | +60.4% | +53.6% to +63.8% | 13 | 13 | +40.6% | 13 |
| FY12E $5.225 (2012-10-17 to 2012-12-28) | 11 | +85.6% | +61.6% to +95.0% | 11 | 11 | +50.2% | 11 |
| latest print Q3 2011 (2012-01-06 to 2012-01-13) | 2 | +44.2% | +43.8% to +44.2% | 2 | 0 | +25.3% | 2 |
| latest print Q4 2011 (2012-01-20 to 2012-04-13) | 13 | +41.5% | +34.3% to +55.3% | 13 | 10 | +23.5% | 13 |
| latest print Q1 2012 (2012-04-20 to 2012-07-13) | 13 | +43.0% | +30.7% to +54.0% | 12 | 2 | +29.6% | 12 |
| latest print Q2 2012 (2012-07-20 to 2012-10-12) | 13 | +60.4% | +53.6% to +63.8% | 13 | 13 | +40.6% | 13 |
| latest print Q3 2012 (2012-10-17 to 2012-12-28) | 11 | +85.6% | +61.6% to +95.0% | 11 | 11 | +50.2% | 11 |

- **CHEAP held on 51 of 52 dates of 2012.** The entries ($51.02-59.51, 9.9-12.7x FY12E) returned +30.7% to +95.0% over two years (median
  +53.6%) against SPY's +33.8% to +55.5%, a strong benchmark: 51 cleared the hurdle but only 36 beat SPY (2 of the 13 dates after the Q1
  2012 print). The miss is 2012-04-20 ($59.51, 12.2x: +30.7%, 9.3pp behind SPY). Over three years +93.6% to +143.2%, all both. FY12E rose
  from $4.65 to $5.225 and FY2012 came in at $5.28; the dates after the Q3 2012 print (FY12E $5.225) returned +61.6% to +95.0%.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 29 | +96.1% | +76.0% to +123.6% | 29 | 29 | +57.9% | 29 |
| class FAIR, legacy tier ACCUMULATE | 19 | +64.7% | +55.5% to +73.4% | 19 | 19 | +52.5% | 0 |
| class FAIR, legacy tier BUY | 5 | +77.9% | +67.2% to +83.8% | 5 | 5 | +55.9% | 0 |
| FY12E $5.225 (2013-01-04 to 2013-01-11) | 2 | +101.0% | +98.2% to +101.0% | 2 | 2 | +60.4% | 2 |
| FY13E $5.375 (2013-01-18 to 2013-07-12) | 26 | +96.1% | +83.8% to +123.6% | 26 | 26 | +57.0% | 25 |
| FY13E $5.425 (2013-07-19 to 2013-10-11) | 13 | +67.3% | +55.5% to +77.9% | 13 | 13 | +48.6% | 0 |
| FY13E $5.45 (2013-10-18 to 2013-12-31) | 12 | +64.7% | +57.4% to +78.9% | 12 | 12 | +59.3% | 2 |
| latest print Q3 2012 (2013-01-04 to 2013-01-11) | 2 | +101.0% | +98.2% to +101.0% | 2 | 2 | +60.4% | 2 |
| latest print Q4 2012 (2013-01-18 to 2013-04-12) | 13 | +104.2% | +90.6% to +123.6% | 13 | 13 | +55.2% | 13 |
| latest print Q1 2013 (2013-04-19 to 2013-07-12) | 13 | +92.8% | +83.8% to +104.0% | 13 | 13 | +57.0% | 12 |
| latest print Q2 2013 (2013-07-19 to 2013-10-11) | 13 | +67.3% | +55.5% to +77.9% | 13 | 13 | +48.6% | 0 |
| latest print Q3 2013 (2013-10-18 to 2013-12-31) | 12 | +64.7% | +57.4% to +78.9% | 12 | 12 | +59.3% | 2 |

- **CHEAP held on all 29 CHEAP dates of 2013; FAIR "failed" on all 24.** The CHEAP entries (2013-01-04 to 2013-07-05 and 2013-10-25,
  2013-11-01; $52.09-68.63, 10.0-12.6x) returned +76.0% to +123.6% over two years; the FAIR ones (from 2013-07-12; $68.00-75.30, 12.6-13.8x
  FY13E) +55.5% to +83.8%, beating SPY by 35.0-58.8pp where FAIR expects a result within 15pp of it. Over three years every 2013 date
  returned +87.0% to +143.6%, clearing both hurdles. Two years on the price was $100.78-123.85 ($122.15 for the first FAIR date), and the
  two-year price landed nearest BULL on 46 dates and BASE on 7: the first dates of the series on which the history's growth path came.
- **The FAIR call came from the window, not the business.** FY13E moved little ($5.375 to $5.45; FY2013 came in at $5.50, the Q4 2013
  release of 2014-01-16, outside the series), BASE was +12.2-13.6% and the proxy composite in its usual 2.0-2.35; what moved was the
  ten-year window, whose median fell from 17.8x (2010) to 11.4x as 2000-2003's multiples left and 2008-2012's entered, and the EPP floor,
  14x to 2011, 13x in 2012, 9x from 2013-01-11. At 12.6-13.8x the price sat at the 53rd-59th percentile of a window made mostly of the
  derated years and 40-54% above a floor set by their lows. Hypothesis, not a rule: when the ten-year window holds mostly a derated regime
  (here the calendar-year lows of 2008-2013 at 5.0-9.5x against 2004-2007's 13.2-18.6x), a recovering business that trades back to the
  window's median reads FAIR before its rerating is done. A five-year window, the pre-outcome sensitivity run, would have read these dates
  RICH. Test it on other tickers with a regime change inside the window; never fit it to UNH.

Across the 209 dates of 2010-2013:
- **CHEAP held on 180 of 185 dates; FAIR on none of 24.** The CHEAP dates returned a median +60.4% over two years and +110.9% over three;
  the FAIR dates +67.0% and +106.5%. Every 2010-2013 date cleared the three-year hurdle and beat SPY over three years.
- **Entry price no longer explains the result.** The correlation of the entry price with the two-year total return is +0.02 (it was -0.81
  in 2008-2009); the ten lowest entries (2010-04-21 to 2010-07-16, $28.30-30.34) returned a median +97.0%, and the 2013 CHEAP entries at
  $52-69 a median +96.1%. The current-year P/E's correlation with it is -0.39. Judge the series by `return_to_avg_price_m12_m24_pct`
  (median +53.8% for 2010, +28.7% for 2011, +34.1% for 2012).
- **The guides were raised, not cut.** Every year's EPS guide rose through the year and the year came in at or above its last guide (FY2010
  $2.90-3.10 to $3.85-3.95, actual $4.10; FY2011 $3.50-3.70 to $4.52-4.57, $4.73; FY2012 $4.55-4.75 to $5.20-5.25, $5.28; FY2013 $5.25-5.50
  to $5.40-5.50, $5.50), and CHEAP held on 180 of 185 dates. This is the other side of the 2008 hypothesis (a CHEAP call on a guide cut in
  successive releases is weaker), and consistent with it, but one stock over two regimes is not a test: try it elsewhere.
- **The guided margin steps pointed the wrong way.** Both schedule-based margins (6.6%-7.1% for 2010, 7.28% derived for 2011) sat a point
  or more under the year's outcome (8.35%, 8.31%), so BASE understated each year; the class did not rest on them (the runs without them
  moved no class before any outcome).
- **The signals added little again.** The proxy composite was 1.85-2.35 on every date. Before any outcome, the signals at BEAR would have
  moved 51 classes from 2011-05-06 (7 CHEAP to FAIR, 20 CHEAP to RICH, the 24 FAIR to RICH): 47 of those dates beat SPY over two years; the
  other 4 are the May-June 2011 misses (0.5-2.1pp behind SPY), where FAIR would have held.
- **Profile drift:** the kind (DURABLE, risk 2) matches today's profile on all 209 dates (a 2026 analysis, read here only through
  `profile_drift`).

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier ACCUMULATE | 7 | +61.2% | +51.9% to +64.3% | 7 | 7 | +61.3% | 0 |
| class FAIR, legacy tier WATCHLIST | 7 | +62.2% | +60.1% to +70.0% | 7 | 7 | +50.2% | 0 |
| class RICH, legacy tier AVOID | 23 | +62.7% | +51.9% to +74.1% | 23 | 23 | +43.7% | 0 |
| class RICH, legacy tier WATCHLIST | 14 | +77.2% | +70.0% to +82.1% | 14 | 14 | +53.1% | 0 |
| FY13E $5.45 (2014-01-10 to 2014-01-10) | 1 | +51.9% | +51.9% to +51.9% | 1 | 1 | +56.4% | 0 |
| FY14E $5.5 (2014-01-17 to 2014-07-11) | 26 | +70.0% | +55.2% to +81.4% | 26 | 26 | +53.1% | 0 |
| FY14E $5.55 (2014-07-18 to 2014-10-10) | 13 | +66.4% | +60.0% to +82.1% | 13 | 13 | +46.5% | 0 |
| FY14E $5.625 (2014-10-17 to 2014-12-26) | 11 | +61.3% | +51.9% to +65.8% | 11 | 11 | +35.3% | 0 |
| latest print Q3 2013 (2014-01-10 to 2014-01-10) | 1 | +51.9% | +51.9% to +51.9% | 1 | 1 | +56.4% | 0 |
| latest print Q4 2013 (2014-01-17 to 2014-04-11) | 13 | +62.2% | +55.2% to +70.0% | 13 | 13 | +55.7% | 0 |
| latest print Q1 2014 (2014-04-17 to 2014-07-11) | 13 | +74.8% | +70.0% to +81.4% | 13 | 13 | +52.6% | 0 |
| latest print Q2 2014 (2014-07-18 to 2014-10-10) | 13 | +66.4% | +60.0% to +82.1% | 13 | 13 | +46.5% | 0 |
| latest print Q3 2014 (2014-10-17 to 2014-12-26) | 11 | +61.3% | +51.9% to +65.8% | 11 | 11 | +35.3% | 0 |

- **Both calls "failed" on all 51 dates: UnitedHealth Group beat SPY over two years on every one.** The 14 FAIR entries (2014-01-10 to
  2014-04-11; $71.36-81.62, 13.0-14.8x the guide) returned +51.9% to +70.0% (SPY by 43.3-56.0pp, where FAIR expects a result within
  15pp); the 37 RICH ones ($75.03-102.55, 13.6-18.2x) +51.9% to +82.1% (SPY by 39.4-66.7pp, where RICH expects a miss of the hurdle and of
  the benchmark). Over three years every 2014 date returned +109.7% to +151.2%. Two years on the price was $109.27-163.03 and landed
  nearest BULL on 44 dates and XBULL on 7.
- **The guide rose all year** ($5.40-5.60 to $5.60-5.65, and FY2014 came in at $5.70), as in 2010-2013, and so did the revenue guide
  ($128-129B to about $130B, actual $130.474B). Nothing in the guide said RICH; the class came from the window (median 11.3-11.4x, the
  floor 9x) against 13-18x.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +58.2% | +42.8% to +96.8% | 53 | 53 | +31.9% | 0 |
| FY14E $5.625 (2015-01-02 to 2015-01-16) | 3 | +60.2% | +57.0% to +63.0% | 3 | 3 | +31.5% | 0 |
| FY15E $6.125 (2015-01-22 to 2015-04-10) | 12 | +49.3% | +42.8% to +56.6% | 12 | 12 | +25.4% | 0 |
| FY15E $6.225 (2015-04-17 to 2015-07-10) | 13 | +54.7% | +44.6% to +58.2% | 13 | 13 | +29.0% | 0 |
| FY15E $6.3 (2015-07-17 to 2015-11-13) | 18 | +69.2% | +54.3% to +95.4% | 18 | 18 | +43.5% | 0 |
| FY15E $6 (2015-11-20 to 2015-12-31) | 7 | +91.9% | +90.1% to +96.8% | 7 | 7 | +57.8% | 0 |
| latest print Q3 2014 (2015-01-02 to 2015-01-16) | 3 | +60.2% | +57.0% to +63.0% | 3 | 3 | +31.5% | 0 |
| latest print Q4 2014 (2015-01-22 to 2015-04-10) | 12 | +49.3% | +42.8% to +56.6% | 12 | 12 | +25.4% | 0 |
| latest print Q1 2015 (2015-04-17 to 2015-07-10) | 13 | +54.7% | +44.6% to +58.2% | 13 | 13 | +29.0% | 0 |
| latest print Q2 2015 (2015-07-17 to 2015-10-09) | 13 | +68.8% | +54.3% to +82.0% | 13 | 13 | +40.6% | 0 |
| latest print Q3 2015 (2015-10-16 to 2015-12-31) | 12 | +90.5% | +65.2% to +96.8% | 12 | 12 | +57.7% | 0 |

- **RICH "failed" on all 53 dates.** $100.78-123.85 at 17.3-19.8x the guide (the 86th-95th percentile) returned +42.8% to +96.8% over two
  years, SPY by 25.1-63.3pp, and +91.1% to +149.1% over three; the two-year price ($157.62-222.77) landed nearest XBULL on every date.
  Even the five dates priced above the BULL case (Ratio B infinite, 2015-03-20 to 2015-06-26) returned +42.8% to +54.1%.
- **The one guide cut of the series came before the best entries of the year.** The 8-K of 2015-11-19 cut FY2015 from $6.25-6.35 to
  "approximately $6.00" (the individual exchange losses); the seven dates on the cut guide ($112.97-118.34, 18.8-19.7x) returned +90.1% to
  +96.8%, the 18 before it on $6.25-6.35 +54.3% to +95.4%. In 2008 the CHEAP calls on successive cuts were the weak ones; here a single
  cut, against a raised guide for the next year ($7.10-7.30), was followed by the strongest returns. The class did not change at the cut
  (RICH either way), so this says nothing about the call; it is a caution against reading "guide cut" as one pattern.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST | 2 | +106.5% | +101.6% to +106.5% | 2 | 2 | +73.7% | 0 |
| class RICH, legacy tier AVOID | 50 | +87.1% | +50.1% to +119.4% | 50 | 50 | +60.0% | 0 |
| FY15E $6 (2016-01-08 to 2016-01-15) | 2 | +114.0% | +108.8% to +114.0% | 2 | 2 | +72.4% | 0 |
| FY16E $7.2 (2016-01-20 to 2016-07-15) | 26 | +86.9% | +69.0% to +119.4% | 26 | 26 | +58.2% | 0 |
| FY16E $7.325 (2016-07-20 to 2016-10-14) | 13 | +94.4% | +80.7% to +105.3% | 13 | 13 | +67.3% | 0 |
| FY16E $7.45 (2016-10-19 to 2016-12-30) | 11 | +79.0% | +50.1% to +93.9% | 11 | 11 | +60.0% | 0 |
| latest print Q3 2015 (2016-01-08 to 2016-01-15) | 2 | +114.0% | +108.8% to +114.0% | 2 | 2 | +72.4% | 0 |
| latest print Q4 2015 (2016-01-20 to 2016-04-15) | 13 | +89.2% | +69.0% to +119.4% | 13 | 13 | +62.0% | 0 |
| latest print Q1 2016 (2016-04-20 to 2016-07-15) | 13 | +86.6% | +78.3% to +91.0% | 13 | 13 | +56.7% | 0 |
| latest print Q2 2016 (2016-07-20 to 2016-10-14) | 13 | +94.4% | +80.7% to +105.3% | 13 | 13 | +67.3% | 0 |
| latest print Q3 2016 (2016-10-19 to 2016-12-30) | 11 | +79.0% | +50.1% to +93.9% | 11 | 11 | +60.0% | 0 |

- **RICH "failed" on all 50 RICH dates and FAIR on both FAIR dates.** The year's two-year returns were the series' highest: +50.1% to
  +119.4% (median +88.0%), SPY by 37.2-67.6pp, the price two years on $212.55-281.36, nearest XBULL on every date. The two FAIR dates
  (2016-02-05 and 2016-02-12, $111.72-111.82, 15.5x) returned +101.6% and +106.5%. BASE was +18.2-21.4%, carried by Catamaran's
  revenue.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +37.7% | +13.6% to +76.0% | 35 | 44 | +37.5% | 8 |
| FY16E $7.45 (2017-01-06 to 2017-01-13) | 2 | +57.0% | +51.4% to +57.0% | 2 | 2 | +53.9% | 0 |
| FY17E $8.9 (2017-01-18 to 2017-04-13) | 13 | +54.8% | +39.3% to +76.0% | 13 | 13 | +54.6% | 0 |
| FY17E $9.2 (2017-04-19 to 2017-07-14) | 13 | +39.3% | +34.9% to +46.0% | 13 | 13 | +42.4% | 0 |
| FY17E $9.275 (2017-07-19 to 2017-10-13) | 13 | +22.2% | +13.6% to +39.3% | 4 | 7 | +30.1% | 6 |
| FY17E $9.45 (2017-10-18 to 2017-12-29) | 11 | +28.5% | +18.6% to +37.7% | 3 | 9 | +16.2% | 2 |
| latest print Q3 2016 (2017-01-06 to 2017-01-13) | 2 | +57.0% | +51.4% to +57.0% | 2 | 2 | +53.9% | 0 |
| latest print Q4 2016 (2017-01-18 to 2017-04-13) | 13 | +54.8% | +39.3% to +76.0% | 13 | 13 | +54.6% | 0 |
| latest print Q1 2017 (2017-04-19 to 2017-07-14) | 13 | +39.3% | +34.9% to +46.0% | 13 | 13 | +42.4% | 0 |
| latest print Q2 2017 (2017-07-19 to 2017-10-13) | 13 | +22.2% | +13.6% to +39.3% | 4 | 7 | +30.1% | 6 |
| latest print Q3 2017 (2017-10-18 to 2017-12-29) | 11 | +28.5% | +18.6% to +37.7% | 3 | 9 | +16.2% | 2 |

- **RICH held on 8 of the 52 dates, all from 2017-09-01 to 2017-11-03** ($192.52-212.87, 20.8-22.5x the guide): they returned +13.6% to
  +21.9% over two years, 0.6-8.1pp behind SPY. On the other 44 the stock beat SPY; the first half's entries ($157.62-187.96, 17.7-21.8x)
  returned +34.9% to +76.0% and cleared the hurdle on all 28, the second half's ($189.19-226.78, 20.4-24.0x) +13.6% to +39.3% and cleared
  it on 7 of 24. Over three years every 2017 date beat SPY (+39.8% to +96.2%). The ten dates above the BULL case (Ratio B infinite, from
  2017-10-27) returned +18.6% to +37.7%, 8 of them ahead of SPY.
- **The late-2017 entries were the first to look expensive in hindsight**, and they were also the first at 20x and more the guide: the
  two-year return falls with the entry multiple across the 208 dates (median +70.0% at 12-15x, +69.0% at 15-19x, +56.1% at 19-21x, +31.9%
  at 21-24x; correlation -0.40), but it stayed positive on every date, and the eight dates that lagged SPY were all at 20.8-22.5x.

Across the 208 dates of 2014-2017:
- **RICH held on 8 of 192 dates; FAIR on none of 16.** The RICH dates returned a median +65.6% over two years and +100.9% over three,
  the FAIR dates +63.1% and +129.3%; UnitedHealth Group beat SPY over two years on 200 of the 208 dates and over three years on all 208,
  and cleared the two-year hurdle on 191. By tier: ACCUMULATE 7 (median +61.2%), WATCHLIST 23 (+74.8%), AVOID 178 (+63.0%). Judged by
  `return_to_avg_price_m12_m24_pct` the medians are +49.2% (2014), +31.9% (2015), +60.4% (2016) and +37.5% (2017).
- **The 2013 hypothesis, extended.** The ten-year window held the 2008-2013 regime on every date (median 11.3-11.4x, the EPP floor 9x,
  set by 2008-2013's calendar-year lows of 5.0-9.5x), while the price tripled and the multiple on the guide rose from 13x to 24x; the
  method read RICH from April 2014 and kept reading it through a +107% median three-year return. The window's median reflected the derating of
  2008-2012 rather than anything in the 2014-2017 filings. Hypothesis, not a rule: a window dominated by a derated regime misreads the rerating that
  follows it, first as FAIR (2013) and then as RICH (2014-2017). Test it on other tickers with a regime change inside the window (and
  against a window that excludes the crisis years); never fit it to UNH.
- **The pre-outcome sensitivity runs do not rescue the calls.** Every date that a tested encoding moved before any outcome (the adjusted
  EPS guides 5, the revenue-guide reading 14, 2007-2008 at GAAP 2, the signals at BEAR 16 and at XBULL 26, a five-year window 24) beat SPY
  over two years; only the 7 moves to CHEAP (the revenue-guide reading's 2, the XBULL signals' 5) would have made a call hold. A five-year
  window, which still holds 2009-2013, moved 24 classes in both directions.
- **The guides were raised in every year (FY2015's then cut once, in November), and each year came in at or above its last guide
  but FY2016 as the 10-K restated it** (FY2014 $5.70 against a last guide of $5.60-5.65; FY2015 $6.01 against the cut "approximately
  $6.00"; FY2016 $7.48 in the Q4 release against "approximately $7.45", $7.25 in the 10-K after the
  Penn Treaty assessments; FY2017 $10.72 in the Q4 2017 release of 2018-01-16, outside the series, against "to approach $9.45", with a
  $1.22 Tax Act benefit). The EPS growth that followed was +3.6% (FY2014), +5.4% (FY2015), +20.6% (FY2016, on the 10-K's $7.25) and
  +47.9% (FY2017; +31.0% without the tax benefit): the price ran ahead of the earnings in 2014-2015 and the earnings caught up in
  2016-2017, so the multiple rerated before the faster earnings growth arrived, and the earnings then carried the price.
- **The Q4 2016 restatement and the adjusted EPS made no difference:** the series' calls are the same with the release's Q4 2016 figures,
  and the adjusted ranges move 5 dates from RICH to FAIR, which beat SPY by more than 15pp either way.
- **Profile drift:** the kind (DURABLE, risk 2) matches today's profile on all 208 dates (a 2026 analysis, read here only through
  `profile_drift`).

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +24.3% | -4.6% to +44.8% | 8 | 33 | +8.2% | 15 |
| FY17E $9.45 (2018-01-05 to 2018-01-12) | 2 | +32.4% | +29.9% to +32.4% | 1 | 2 | +9.8% | 0 |
| FY18E $11.8 (2018-01-17 to 2018-04-13) | 13 | +21.0% | -4.6% to +34.3% | 3 | 13 | +12.9% | 0 |
| FY18E $11.825 (2018-04-18 to 2018-07-13) | 13 | +24.1% | +14.6% to +29.0% | 0 | 13 | +6.5% | 0 |
| FY18E $11.925 (2018-07-18 to 2018-10-12) | 13 | +20.2% | +15.4% to +30.4% | 0 | 5 | +5.1% | 8 |
| FY18E $12.1 (2018-10-17 to 2018-12-28) | 11 | +30.2% | +22.3% to +44.8% | 4 | 0 | +11.3% | 7 |
| latest print Q3 2017 (2018-01-05 to 2018-01-12) | 2 | +32.4% | +29.9% to +32.4% | 1 | 2 | +9.8% | 0 |
| latest print Q4 2017 (2018-01-17 to 2018-04-13) | 13 | +21.0% | -4.6% to +34.3% | 3 | 13 | +12.9% | 0 |
| latest print Q1 2018 (2018-04-18 to 2018-07-13) | 13 | +24.1% | +14.6% to +29.0% | 0 | 13 | +6.5% | 0 |
| latest print Q2 2018 (2018-07-18 to 2018-10-12) | 13 | +20.2% | +15.4% to +30.4% | 0 | 5 | +5.1% | 8 |
| latest print Q3 2018 (2018-10-17 to 2018-12-28) | 11 | +30.2% | +22.3% to +44.8% | 4 | 0 | +11.3% | 7 |

- **RICH held on 15 of 52 dates, all from 2018-08-24** ($238.34-281.36). The 33 entries to 2018-08-17 ($212.55-262.33, 18.0-24.2x)
  returned -4.6% to +34.3% over two years and beat SPY on every one, by 0.1-22.2pp, while clearing the hurdle on 4; the 28 from
  2018-08-24 to 2018-12-28 (19.7-23.3x) returned +15.4% to +44.8% and lagged SPY on every one, by 0.4-14.1pp (RICH held on 15 of
  them, where the hurdle was missed too; the lag runs on to 2019-03-01, 0.4-21.3pp over the 28 dates from 2018-08-24). The year's 1-year median was +0.8%; every 2018 entry sat through the -36.2% drawdown of
  February-March 2020, and two years on the price was $194.86-356.82, nearest BULL on 49 dates. The only negative two-year return of
  the series is 2018-03-23 (-4.6%, still 4.7pp ahead of SPY).

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 2 | +86.9% | +84.6% to +86.9% | 2 | 2 | +69.4% | 2 |
| class CHEAP, legacy tier BUY | 2 | +92.9% | +80.7% to +92.9% | 2 | 2 | +73.2% | 2 |
| class FAIR, legacy tier ACCUMULATE | 9 | +81.7% | +71.0% to +88.9% | 9 | 9 | +57.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 12 | +69.7% | +66.0% to +78.8% | 12 | 12 | +40.1% | 1 |
| class RICH, legacy tier ACCUMULATE | 1 | +87.6% | +87.6% to +87.6% | 1 | 1 | +55.2% | 0 |
| class RICH, legacy tier AVOID | 15 | +49.6% | +24.4% to +72.3% | 11 | 7 | +25.8% | 4 |
| class RICH, legacy tier WATCHLIST | 11 | +57.1% | +39.6% to +84.0% | 11 | 9 | +30.8% | 0 |
| FY18E $12.1 (2019-01-04 to 2019-01-11) | 2 | +49.6% | +49.3% to +49.6% | 2 | 0 | +25.8% | 0 |
| FY19E $13.85 (2019-01-16 to 2019-04-12) | 13 | +39.6% | +24.4% to +72.7% | 9 | 5 | +24.1% | 4 |
| FY19E $13.925 (2019-04-17 to 2019-07-12) | 13 | +69.7% | +60.1% to +84.6% | 13 | 13 | +38.2% | 1 |
| FY19E $14.05 (2019-07-19 to 2019-10-11) | 13 | +81.5% | +63.2% to +92.9% | 13 | 13 | +57.2% | 4 |
| FY19E $14.2 (2019-10-16 to 2019-11-29) | 7 | +83.9% | +61.7% to +87.6% | 7 | 7 | +49.9% | 0 |
| FY19E $14.25 (2019-12-06 to 2019-12-27) | 4 | +71.1% | +67.9% to +72.3% | 4 | 4 | +38.6% | 0 |
| latest print Q3 2018 (2019-01-04 to 2019-01-11) | 2 | +49.6% | +49.3% to +49.6% | 2 | 0 | +25.8% | 0 |
| latest print Q4 2018 (2019-01-16 to 2019-04-12) | 13 | +39.6% | +24.4% to +72.7% | 9 | 5 | +24.1% | 4 |
| latest print Q1 2019 (2019-04-17 to 2019-07-12) | 13 | +69.7% | +60.1% to +84.6% | 13 | 13 | +38.2% | 1 |
| latest print Q2 2019 (2019-07-19 to 2019-10-11) | 13 | +81.5% | +63.2% to +92.9% | 13 | 13 | +57.2% | 4 |
| latest print Q3 2019 (2019-10-16 to 2019-12-27) | 11 | +71.1% | +61.7% to +87.6% | 11 | 11 | +40.7% | 0 |

- **CHEAP held on all 4 CHEAP dates, RICH on 4 of 27, FAIR on 1 of 21.** The FAIR and CHEAP entries (2019-04-12 to 2019-10-16,
  $215.26-252.94, 15.3-18.0x) returned +66.0% to +92.9% over two years, SPY by 13.7-39.3pp (FAIR held only on 2019-08-09, 13.7pp
  ahead), and +93.9% to +153.6% over three; the CHEAP ones +80.7% to +92.9%. The RICH entries ($237.29-295.97, 17.1-20.8x) returned
  +24.4% to +87.6% and beat SPY on 17 of 27. Every 2019 entry beat SPY over three years.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 3 | +128.1% | +116.1% to +150.2% | 3 | 3 | +90.6% | 3 |
| class FAIR, legacy tier ACCUMULATE | 1 | +90.7% | +90.7% to +90.7% | 1 | 1 | +66.3% | 0 |
| class RICH, legacy tier ACCUMULATE | 2 | +110.8% | +74.9% to +110.8% | 2 | 2 | +66.8% | 0 |
| class RICH, legacy tier AVOID | 25 | +62.5% | +50.0% to +78.1% | 25 | 25 | +49.6% | 0 |
| class RICH, legacy tier WATCHLIST | 22 | +77.2% | +59.1% to +84.5% | 22 | 22 | +56.2% | 0 |
| FY19E $14.25 (2020-01-03 to 2020-01-10) | 2 | +77.1% | +61.1% to +77.1% | 2 | 2 | +39.6% | 0 |
| FY20E $15.6 (2020-01-16 to 2020-10-09) | 39 | +74.9% | +57.5% to +150.2% | 39 | 39 | +55.2% | 3 |
| FY20E $15.775 (2020-10-15 to 2020-11-27) | 7 | +61.8% | +50.0% to +84.5% | 7 | 7 | +50.4% | 0 |
| FY20E $15.9 (2020-12-04 to 2020-12-31) | 5 | +58.3% | +54.6% to +63.5% | 5 | 5 | +49.6% | 0 |
| latest print Q3 2019 (2020-01-03 to 2020-01-10) | 2 | +77.1% | +61.1% to +77.1% | 2 | 2 | +39.6% | 0 |
| latest print Q4 2019 (2020-01-16 to 2020-04-09) | 13 | +79.3% | +58.7% to +150.2% | 13 | 13 | +51.5% | 3 |
| latest print Q1 2020 (2020-04-16 to 2020-07-10) | 13 | +76.7% | +59.1% to +82.8% | 13 | 13 | +56.2% | 0 |
| latest print Q2 2020 (2020-07-16 to 2020-10-09) | 13 | +72.9% | +57.5% to +82.8% | 13 | 13 | +54.8% | 0 |
| latest print Q3 2020 (2020-10-15 to 2020-12-31) | 12 | +61.7% | +50.0% to +84.5% | 12 | 12 | +50.4% | 0 |

- **CHEAP held on all 3 CHEAP dates; RICH on none of 49.** The COVID-low entries (2020-03-20 to 2020-04-03, $206.59-242.45,
  13.2-15.5x) returned +116.1% to +150.2% over two years, the series' best; the RICH ones ($264.13-355.67, 16.9-22.5x) +50.0% to
  +110.8%, SPY by 14.7-61.7pp, every one clearing the hurdle. The guide was "maintained" through the pandemic and FY2020 came in at
  $16.03 against "to approach $15.90".

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 47 | +24.2% | +7.6% to +42.8% | 7 | 47 | +22.8% | 0 |
| class RICH, legacy tier WATCHLIST | 5 | +49.4% | +49.2% to +57.5% | 5 | 5 | +56.0% | 0 |
| FY20E $15.9 (2021-01-08 to 2021-01-15) | 2 | +42.8% | +38.1% to +42.8% | 2 | 2 | +45.5% | 0 |
| FY21E $17.15 (2021-01-21 to 2021-04-09) | 12 | +41.3% | +29.7% to +57.5% | 9 | 12 | +47.7% | 0 |
| FY21E $17.4 (2021-04-16 to 2021-07-09) | 13 | +21.3% | +15.1% to +34.1% | 1 | 13 | +25.1% | 0 |
| FY21E $17.6 (2021-07-16 to 2021-10-08) | 13 | +24.2% | +15.7% to +31.9% | 0 | 13 | +21.3% | 0 |
| FY21E $17.825 (2021-10-15 to 2021-11-26) | 7 | +20.8% | +16.8% to +29.1% | 0 | 7 | +11.1% | 0 |
| FY21E $17.875 (2021-12-03 to 2021-12-31) | 5 | +11.8% | +7.6% to +24.8% | 0 | 5 | +2.6% | 0 |
| latest print Q3 2020 (2021-01-08 to 2021-01-15) | 2 | +42.8% | +38.1% to +42.8% | 2 | 2 | +45.5% | 0 |
| latest print Q4 2020 (2021-01-21 to 2021-04-09) | 12 | +41.3% | +29.7% to +57.5% | 9 | 12 | +47.7% | 0 |
| latest print Q1 2021 (2021-04-16 to 2021-07-09) | 13 | +21.3% | +15.1% to +34.1% | 1 | 13 | +25.1% | 0 |
| latest print Q2 2021 (2021-07-16 to 2021-10-08) | 13 | +24.2% | +15.7% to +31.9% | 0 | 13 | +21.3% | 0 |
| latest print Q3 2021 (2021-10-15 to 2021-12-31) | 12 | +20.3% | +7.6% to +29.1% | 0 | 12 | +9.4% | 0 |

- **RICH held on none of 52 dates, but on its own terms it was close.** UnitedHealth Group beat SPY over two years on all 52 (SPY's 2022
  fall), by 4.4-50.0pp, yet cleared the hurdle only on 12, all to 2021-04-16; the 38 entries from 2021-04-16 ($389.37-502.14, 22.3-28.1x,
  the series' highest multiples) returned +7.6% to +34.1% over two years and +4.2% to +54.0% over three, and lagged SPY over three years
  on 16 dates from 2021-04-09. The last date, 2021-12-31 at $502.14 (28.1x), returned +7.6% over two years and +5.5% over three. Two
  years on every 2021 price landed nearest BULL.

Across the 209 dates of 2018-2021:
- **CHEAP held on all 7 dates, FAIR on 1 of 22, RICH on 19 of 180.** Median two-year returns: CHEAP +92.9%, FAIR +73.8%, RICH +32.8%
  (three years: +139.3%, +121.9%, +65.3%). UnitedHealth Group beat SPY over two years on 180 of the 209 dates and over three on 181, and
  cleared the two-year hurdle on 121.
- **The tiers ranked the returns in order, though the classes missed their own expectations:** BUY 5 (median +116.1%), ACCUMULATE 15
  (+84.6%), WATCHLIST 50 (+70.5%), AVOID 139 (+27.2%). The entry multiple explains more than in 2014-2017: the correlation of the
  current-year P/E with the two-year return is -0.75 (it was -0.40), from a median +92.9% at 13-16x to +17.8% at 25-28x. RICH was
  right about the direction against the stock's own better entries and wrong against the market: the AVOID dates still beat SPY on 112
  of 139.
- **The 2013 and 2014-2017 hypothesis, as the window cleared.** The window's median rose from 11.3x to 18.0x as 2008-2012 left it, and
  RICH began to hold where the multiple was highest (late 2018, the 2021 entries' three-year returns), but most RICH calls still failed
  against a market the stock beat. The pre-outcome runs point the same way: the five-year window, which leaves out more of the derated
  years, moved 75 classes (mostly to CHEAP), and 68 of the moved dates would then have held, against 5 before; the signals at XBULL moved
  68 (29 then held, 3 before), the adjusted guides 18 (15 then held, none before), FY2017 at $9.50 6 (all 6 then held). The signals at
  BEAR, which moved the 29 FAIR and CHEAP dates to RICH, would have turned 8 holds into none. Hypothesis, not a rule, and the same one as
  before: a ten-year window that still holds a derated regime reads a rerated franchise as dear; test it on other tickers, never fit it to
  UNH.
- **The guides were raised in every year and met:** FY2018 $12.19 against "to approach $12.10", FY2019 $14.33 against "to approach
  $14.25", FY2020 $16.03 against "to approach $15.90", and FY2021 $18.08 (the Q4 2021 release of 2022-01-19, outside the series)
  against $17.80-17.95. The COVID-19 allowance in the FY2021 ranges was not needed in the end; adding it back (before any outcome) moved 5
  dates from RICH to FAIR, none of which then held.
- **FY2017 with its Tax Reform benefit** set XBULL at +33.6%/yr on every date from the Q4 2017 print; the realized two-year EPS growth
  from FY2017 to FY2019 was +15.6%/yr on GAAP ($10.72 to $14.33), +22.8% on the $9.50 reading. BULL (+14.5-16.0%) was closer than XBULL,
  and two-year prices landed nearest BULL or XBULL on every date but one (BASE, in 2018).
- **Profile drift:** the kind (DURABLE, risk 2) matches today's profile on all 209 dates (a 2026 analysis, read here only through
  `profile_drift`).
