# UNH retrospective findings (hindsight)

Patterns seen in `outcome.json` for the UNH weekly dates: 314, 105 from 2008-01-04 to 2009-12-31 and 209 from 2010-01-08 to 2013-12-31,
all UnitedHealth Group Incorporated (NYSE: UNH). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build, validation, README section and firewall result were committed and pushed (95bb426, the builder fix the firewall's first
run needed 36eb1c4, firewall result 4a203a3); the outcomes were computed on 2026-11-24. Every date has its 6-month, 1-, 2- and 3-year
horizons (the last ends 2012-12-28 for 2008-2009 and 2016-12-30 for 2010-2013). The 2010-2013 batch was decided in the session that
scored 2008-2009 (disclosed in retro/README.md, "UNH 2010-2013") and scored only after its build, validation outputs, README section and
firewall result were committed and pushed (5ed6613, 237ded5, 5fcd318, ac1542c), on 2026-11-24. Total returns include the dividends (the
annual $0.03 to the ex-date of 2010-04-01, then quarterly: $0.125 from 2010-06-03, $0.163 from 2011-06-03, $0.213 from 2012-06-13, $0.28
from 2013-06-13, $0.375 from 2014-06-12, $0.50 from 2015-06-11, $0.625 from 2016-06-15). No split falls in any horizon, so every price
is as traded.
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1%
over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within 15pp of
it either way. Every 2008-2012 date was CHEAP and BUY, so those tables test that one call against the calendar; 2013 has 29 CHEAP and
BUY dates and 24 FAIR (5 BUY, 19 ACCUMULATE).

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
