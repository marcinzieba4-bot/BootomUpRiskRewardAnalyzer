# OKE retrospective findings (hindsight)

Patterns seen in `outcome.json` for the OKE weekly dates: 105 from 2008-01-04 to 2009-12-31, all ONEOK, Inc. (NYSE: OKE). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time build,
validation outputs, README section and firewall result were committed and pushed (a35536d6e, 0476fad08, 2f5bd1051, 8aa12c98d), on
2026-11-28. The one-line 2026 profile that `retro_tool outcome` copies into each `outcome.json` (`profile_drift`: today DURABLE, risk 2,
"ONEOK: midstream NGL/gas; acquisition-driven, leverage") was first seen there, after every model had been built, validated and committed.
Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include the dividends ($0.36-$0.42 a quarter in the range). The
15%/yr hurdle is +32.2% over two years. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), RICH
should miss the hurdle and lag it, FAIR sits between.

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier WATCHLIST (2008-01-04 to 2008-02-15) | 5 | +2.2% | -6.5% to +10.0% | 0 | 5 | -29.3% | 0 |
| class RICH, legacy tier AVOID (2008-01-11 to 2008-02-22) | 3 | -1.9% | -3.0% to +3.1% | 0 | 3 | -31.5% | 0 |
| class FAIR, legacy tier ACCUMULATE (2008-02-27 to 2008-06-20) | 11 | +0.2% | -6.3% to +9.9% | 0 | 11 | -20.8% | 4 |
| class CHEAP, legacy tier BUY (2008-03-07 to 2008-12-26) | 29 | +24.2% | +6.0% to +122.3% | 14 | 29 | +14.5% | 29 |
| class FAIR, legacy tier BUY (2008-06-27 to 2008-07-18) | 4 | +2.3% | -4.2% to +6.0% | 0 | 4 | -13.0% | 3 |
| FY07E $2.67 (the Q3 2007 release's $2.62-2.72) (2008-01-04 to 2008-01-04) | 1 | +10.0% | +10.0% to +10.0% | 0 | 1 | -28.8% | 0 |
| FY07E $2.77 (the 8-K of 2008-01-10's $2.75-2.79) (2008-01-11 to 2008-02-22) | 7 | -1.9% | -6.5% to +7.1% | 0 | 7 | -29.7% | 0 |
| FY08E $2.95 (the 8-K of 2008-01-10's $2.75-3.15) (2008-02-27 to 2008-04-25) | 9 | +8.6% | -1.0% to +10.9% | 0 | 9 | -23.1% | 7 |
| FY08E $2.95 (the Q1 2008 release's $2.75-3.15) (2008-05-02 to 2008-08-01) | 14 | +1.7% | -6.3% to +10.9% | 0 | 14 | -16.5% | 8 |
| FY08E $3.00 (the Q2 2008 release's $2.90-3.10) (2008-08-07 to 2008-10-31) | 13 | +24.2% | +7.9% to +122.3% | 6 | 13 | +14.5% | 13 |
| FY08E $3.00 (the Q3 2008 release's $2.95-3.05) (2008-11-07 to 2008-12-26) | 8 | +109.7% | +82.4% to +113.7% | 8 | 8 | +68.9% | 8 |
| latest print Q3 2007 (2008-01-04 to 2008-02-22) | 8 | +2.2% | -6.5% to +10.0% | 0 | 8 | -29.6% | 0 |
| latest print Q4 2007 (2008-02-27 to 2008-04-25) | 9 | +8.6% | -1.0% to +10.9% | 0 | 9 | -23.1% | 7 |
| latest print Q1 2008 (2008-05-02 to 2008-08-01) | 14 | +1.7% | -6.3% to +10.9% | 0 | 14 | -16.5% | 8 |
| latest print Q2 2008 (2008-08-07 to 2008-10-31) | 13 | +24.2% | +7.9% to +122.3% | 6 | 13 | +14.5% | 13 |
| latest print Q3 2008 (2008-11-07 to 2008-12-26) | 8 | +109.7% | +82.4% to +113.7% | 8 | 8 | +68.9% | 8 |
3y (52 dates with one): 34 of 52 cleared, 52 beat SPY; range +28.0% to +238.9%

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-02 to 2009-07-17) | 29 | +171.5% | +92.6% to +259.8% | 29 | 29 | +95.4% | 29 |
| class RICH, legacy tier BUY (2009-07-24 to 2009-11-05) | 10 | +111.2% | +96.3% to +138.6% | 10 | 10 | +77.9% | 0 |
| class RICH, legacy tier ACCUMULATE (2009-09-18 to 2009-12-04) | 10 | +105.9% | +91.0% to +121.3% | 10 | 10 | +68.9% | 0 |
| class RICH, legacy tier WATCHLIST (2009-12-11 to 2009-12-31) | 4 | +105.6% | +101.3% to +106.4% | 4 | 4 | +60.0% | 0 |
| FY08E $3.00 (the Q3 2008 release's $2.95-3.05) (2009-01-02 to 2009-02-06) | 6 | +113.3% | +92.6% to +123.1% | 6 | 6 | +63.7% | 6 |
| FY08E $3.00 (the 8-K of 2009-02-09's $2.95-3.05) (2009-02-13 to 2009-02-20) | 2 | +180.3% | +128.9% to +180.3% | 2 | 2 | +100.9% | 2 |
| FY09E $2.50 (the 8-K of 2009-02-09's $2.25-2.75) (2009-02-25 to 2009-04-24) | 9 | +194.8% | +171.5% to +259.8% | 9 | 9 | +114.6% | 9 |
| FY09E $2.50 (the Q1 2009 release's $2.25-2.75) (2009-05-01 to 2009-07-31) | 14 | +161.1% | +131.5% to +178.6% | 14 | 14 | +90.1% | 12 |
| FY09E $2.55 (the Q2 2009 release's $2.40-2.70) (2009-08-06 to 2009-10-30) | 13 | +102.1% | +91.0% to +121.3% | 13 | 13 | +74.9% | 0 |
| FY09E $2.75 (the Q3 2009 release's $2.65-2.85) (2009-11-05 to 2009-12-31) | 9 | +106.4% | +101.3% to +114.1% | 9 | 9 | +64.9% | 0 |
| latest print Q3 2008 (2009-01-02 to 2009-02-20) | 8 | +114.3% | +92.6% to +180.3% | 8 | 8 | +65.7% | 8 |
| latest print Q4 2008 (2009-02-25 to 2009-04-24) | 9 | +194.8% | +171.5% to +259.8% | 9 | 9 | +114.6% | 9 |
| latest print Q1 2009 (2009-05-01 to 2009-07-31) | 14 | +161.1% | +131.5% to +178.6% | 14 | 14 | +90.1% | 12 |
| latest print Q2 2009 (2009-08-06 to 2009-10-30) | 13 | +102.1% | +91.0% to +121.3% | 13 | 13 | +74.9% | 0 |
| latest print Q3 2009 (2009-11-05 to 2009-12-31) | 9 | +106.4% | +101.3% to +114.1% | 9 | 9 | +64.9% | 0 |
3y (53 dates with one): 53 of 53 cleared, 53 beat SPY; range +103.4% to +366.8%


## What the labels suggest (hypotheses only)

- **The CHEAP calls held on all 58 dates** (29 in each year) and the RICH calls on none of the 32; FAIR held on 7 of 15. In all, 65 of 105.
  Every 2009 entry more than doubled over two years (+91% to +260%), and every 2008 entry beat SPY over two years (by 10-86 points) and
  over three.
- **The RICH dates were wrong in both years, for different reasons.** The 8 of January-February 2008 (16-17x the FY2007 guide's
  midpoint, the 79th-91st percentile) returned -6.5% to +10% over two years, under the hurdle but 10-26 points ahead of a falling market;
  under `call_check_2y` a RICH call must also lag SPY, so none held, though the multiple did compress (m12-24 average price -28% to -34%).
  The 24 from 2009-07-24 rested on BASE's -44% to -47%/yr, the latest quarter's revenues halving with gas and NGL prices while net
  margin held; they returned +91% to +139%. Revenues as reported were the wrong growth read for a company whose revenues are mostly
  commodity pass-through (the sensitivity's 28 classes on net margin are the hypothesis to test, never a change to this archive).
- **The best entries were the deepest discounts:** the CHEAP dates from the Q3 2008 print to April 2009 (9-10x the guide, the price under
  the EPP floor on 13 dates) returned +82% to +260% over two years. The FAIR and CHEAP dates of March-July 2008 (15-17x) returned -6% to
  +11%: CHEAP there meant cheap against a +27-49%/yr BASE that commodity revenues had inflated, and the call held only because the market
  fell further.
- **The drawdowns were large on every 2008 entry** (-42% to -64% within two years); CHEAP did not mean safe in 2008.
- **The kind held:** DURABLE then (no 10-K called the business cyclical), DURABLE in today's profile. Label only.
- One stock and two years: the pattern "BASE on commodity revenues misreads a margin business" is a hypothesis to test on other
  midstream and distribution names, not a rule.

# OKE 2010-2013 (hindsight)

Patterns seen in `outcome.json` for the 209 weekly dates from 2010-01-08 to 2013-12-31. **Labels and hypotheses**: never feed them back into
the method or the fact sheet. Scored only after the point-in-time build, validation outputs, README section and firewall result were
committed and pushed (e59000592, 9fcac8124, 052f40fba, 7940d4dc3), on 2026-11-28; the 2008-2009 findings above were first opened then.
Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include the dividends paid. "Call held" is `call_check_2y`: CHEAP
should clear the 15%/yr hurdle (+32.2% over two years) or beat SPY, RICH should miss the hurdle and lag it, FAIR sits between. For the
dates before 2014-02-03 the horizons cross the ONE Gas separation, which Yahoo records as an 11422:10000 factor: `retro_tool outcome`
multiplies the later prices and dividends by it, so the ONE Gas shares count as reinvested in OKE at the distribution, not at their own
later prices.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2010-01-08 to 2010-01-08) | 1 | +100.9% | +100.9% to +100.9% | 1 | 1 | +54.2% | 0 |
| class RICH, legacy tier WATCHLIST (2010-01-15 to 2010-12-31) | 6 | +70.1% | +60.2% to +106.6% | 6 | 6 | +58.8% | 0 |
| class RICH, legacy tier ACCUMULATE (2010-01-29 to 2010-02-19) | 4 | +110.7% | +100.6% to +111.5% | 4 | 4 | +74.2% | 0 |
| class CHEAP, legacy tier BUY (2010-02-24 to 2010-09-24) | 29 | +97.4% | +77.3% to +124.1% | 29 | 29 | +72.6% | 29 |
| class CHEAP, legacy tier ACCUMULATE (2010-04-23 to 2010-10-01) | 3 | +99.1% | +72.5% to +120.6% | 3 | 3 | +69.5% | 3 |
| class FAIR, legacy tier ACCUMULATE (2010-10-08 to 2010-11-19) | 6 | +97.4% | +89.0% to +113.3% | 6 | 6 | +72.1% | 0 |
| class FAIR, legacy tier WATCHLIST (2010-11-12 to 2010-12-03) | 3 | +79.3% | +77.4% to +88.6% | 3 | 3 | +66.3% | 0 |
| FY09E $2.75 (the Q3 2009 release's $2.65-2.85) (2010-01-08 to 2010-01-22) | 3 | +105.2% | +100.9% to +106.6% | 3 | 3 | +57.3% | 0 |
| FY09E $2.87 (the 8-K of 2010-01-25's $2.85-2.89) (2010-01-29 to 2010-02-19) | 4 | +110.7% | +100.6% to +111.5% | 4 | 4 | +74.2% | 0 |
| FY10E $2.982 (the 8-K of 2010-01-25's $300-335 million) (2010-02-24 to 2010-04-23) | 9 | +86.1% | +72.5% to +100.5% | 9 | 9 | +59.5% | 9 |
| FY10E $2.956 (the Q1 2010 release's $300-335 million) (2010-04-30 to 2010-07-30) | 14 | +97.4% | +83.6% to +112.3% | 14 | 14 | +73.6% | 14 |
| FY10E $2.944 (the Q2 2010 release's $300-335 million) (2010-08-05 to 2010-10-01) | 9 | +112.1% | +99.1% to +124.1% | 9 | 9 | +83.7% | 9 |
| FY10E $3.037 (the 8-K of 2010-10-05's $320-335 million) (2010-10-08 to 2010-10-29) | 4 | +103.1% | +97.2% to +113.3% | 4 | 4 | +72.2% | 0 |
| FY10E $3.042 (the Q3 2010 release's $320-335 million) (2010-11-04 to 2010-12-31) | 9 | +77.4% | +60.2% to +89.7% | 9 | 9 | +64.0% | 0 |
| latest print Q3 2009 (2010-01-08 to 2010-02-19) | 7 | +105.2% | +100.6% to +111.5% | 7 | 7 | +69.7% | 0 |
| latest print Q4 2009 (2010-02-24 to 2010-04-23) | 9 | +86.1% | +72.5% to +100.5% | 9 | 9 | +59.5% | 9 |
| latest print Q1 2010 (2010-04-30 to 2010-07-30) | 14 | +97.4% | +83.6% to +112.3% | 14 | 14 | +73.6% | 14 |
| latest print Q2 2010 (2010-08-05 to 2010-10-29) | 13 | +111.8% | +97.2% to +124.1% | 13 | 13 | +82.3% | 9 |
| latest print Q3 2010 (2010-11-04 to 2010-12-31) | 9 | +77.4% | +60.2% to +89.7% | 9 | 9 | +64.0% | 0 |
3y (52 dates with one): 52 of 52 cleared, 52 beat SPY; range +98.8% to +154.4%

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier WATCHLIST (2011-01-07 to 2011-01-07) | 1 | +67.2% | +67.2% to +67.2% | 1 | 1 | +56.1% | 0 |
| class RICH, legacy tier AVOID (2011-01-14 to 2011-12-30) | 51 | +53.7% | +15.5% to +74.6% | 46 | 39 | +33.9% | 5 |
| FY10E $3.042 (the Q3 2010 release's $320-335 million) (2011-01-07 to 2011-02-18) | 7 | +67.2% | +55.3% to +68.5% | 7 | 7 | +48.7% | 0 |
| FY11E $3.182 (the 8-K of 2011-01-21's $325-360 million) (2011-02-23 to 2011-04-29) | 10 | +53.7% | +45.7% to +60.9% | 10 | 10 | +36.6% | 0 |
| FY11E $3.137 (the Q1 2011 release's $325-360 million) (2011-05-05 to 2011-07-29) | 13 | +35.2% | +15.5% to +49.3% | 8 | 8 | +29.3% | 5 |
| FY11E $3.101 (the Q2 2011 release's $325-345 million) (2011-08-04 to 2011-09-23) | 8 | +64.2% | +57.8% to +74.6% | 8 | 8 | +40.7% | 0 |
| FY11E $3.101 (the 8-K of 2011-09-29's $325-345 million) (2011-09-30 to 2011-10-28) | 5 | +63.3% | +55.0% to +69.5% | 5 | 5 | +33.9% | 0 |
| FY11E $3.35 (the Q3 2011 release's $345-365 million) (2011-11-03 to 2011-12-30) | 9 | +49.7% | +44.2% to +59.6% | 9 | 2 | +20.3% | 0 |
| latest print Q3 2010 (2011-01-07 to 2011-02-18) | 7 | +67.2% | +55.3% to +68.5% | 7 | 7 | +48.7% | 0 |
| latest print Q4 2010 (2011-02-23 to 2011-04-29) | 10 | +53.7% | +45.7% to +60.9% | 10 | 10 | +36.6% | 0 |
| latest print Q1 2011 (2011-05-05 to 2011-07-29) | 13 | +35.2% | +15.5% to +49.3% | 8 | 8 | +29.3% | 5 |
| latest print Q2 2011 (2011-08-04 to 2011-10-28) | 13 | +63.3% | +55.0% to +74.6% | 13 | 13 | +39.0% | 0 |
| latest print Q3 2011 (2011-11-03 to 2011-12-30) | 9 | +49.7% | +44.2% to +59.6% | 9 | 2 | +20.3% | 0 |
3y (52 dates with one): 48 of 52 cleared, 45 beat SPY; range +35.9% to +155.4%

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2012-01-06 to 2012-12-28) | 52 | +72.3% | +28.5% to +92.7% | 51 | 46 | +42.6% | 1 |
| FY11E $3.35 (the Q3 2011 release's $345-365 million) (2012-01-06 to 2012-01-20) | 3 | +48.8% | +48.0% to +59.0% | 3 | 3 | +15.2% | 0 |
| FY11E $3.397 (the 8-K of 2012-01-23's $355-365 million) (2012-01-27 to 2012-02-17) | 4 | +73.1% | +59.6% to +73.9% | 4 | 4 | +27.8% | 0 |
| FY12E $3.638 (the Q4 2011 release's $360-410 million) (2012-02-22 to 2012-04-27) | 10 | +73.4% | +68.7% to +75.5% | 10 | 10 | +32.9% | 0 |
| FY12E $3.635 (the Q1 2012 release's $360-410 million) (2012-05-03 to 2012-06-01) | 5 | +83.0% | +71.0% to +92.7% | 5 | 5 | +39.5% | 0 |
| FY12E $1.817 (the Q1 2012 release's $360-410 million) (2012-06-08 to 2012-07-27) | 8 | +85.5% | +75.6% to +90.2% | 8 | 8 | +43.8% | 0 |
| FY12E $1.70 (the Q2 2012 release's $345-375 million) (2012-08-02 to 2012-09-21) | 8 | +79.4% | +69.7% to +88.1% | 8 | 8 | +45.9% | 0 |
| FY12E $1.70 (the 8-K of 2012-09-25's $345-375 million) (2012-09-28 to 2012-10-26) | 5 | +55.4% | +45.1% to +63.8% | 5 | 5 | +44.0% | 0 |
| FY12E $1.715 (the Q3 2012 release's $345-375 million) (2012-11-01 to 2012-12-28) | 9 | +48.4% | +28.5% to +54.3% | 8 | 3 | +56.1% | 1 |
| latest print Q3 2011 (2012-01-06 to 2012-02-17) | 7 | +59.6% | +48.0% to +73.9% | 7 | 7 | +20.6% | 0 |
| latest print Q4 2011 (2012-02-22 to 2012-04-27) | 10 | +73.4% | +68.7% to +75.5% | 10 | 10 | +32.9% | 0 |
| latest print Q1 2012 (2012-05-03 to 2012-07-27) | 13 | +83.4% | +71.0% to +92.7% | 13 | 13 | +42.3% | 0 |
| latest print Q2 2012 (2012-08-02 to 2012-10-26) | 13 | +71.6% | +45.1% to +88.1% | 13 | 13 | +44.9% | 0 |
| latest print Q3 2012 (2012-11-01 to 2012-12-28) | 9 | +48.4% | +28.5% to +54.3% | 8 | 3 | +56.1% | 1 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -29.6% to +49.6%

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2013-01-04 to 2013-12-31) | 53 | +12.7% | -55.1% to +37.3% | 1 | 0 | +30.2% | 52 |
| FY12E $1.715 (the Q3 2012 release's $345-375 million) (2013-01-04 to 2013-02-22) | 8 | +20.8% | +12.7% to +37.3% | 1 | 0 | +45.2% | 7 |
| FY13E $1.792 (the Q4 2012 release's $350-400 million) (2013-02-27 to 2013-04-26) | 9 | +21.6% | +18.3% to +28.4% | 0 | 0 | +39.0% | 9 |
| FY13E $1.79 (the Q1 2013 release's $350-400 million) (2013-05-02 to 2013-06-07) | 6 | +16.2% | +12.1% to +27.7% | 0 | 0 | +37.8% | 6 |
| FY13E $1.241 (the 8-K of 2013-06-12's $235-285 million) (2013-06-14 to 2013-07-26) | 7 | +16.4% | -8.7% to +23.4% | 0 | 0 | +40.2% | 7 |
| FY13E $1.245 (the Q2 2013 release's $235-285 million) (2013-08-01 to 2013-11-01) | 14 | -11.8% | -22.1% to -7.6% | 0 | 0 | +5.1% | 14 |
| FY13E $1.239 (the Q3 2013 release's $245-275 million) (2013-11-07 to 2013-12-31) | 9 | -43.8% | -55.1% to -27.6% | 0 | 0 | -21.4% | 9 |
| latest print Q3 2012 (2013-01-04 to 2013-02-22) | 8 | +20.8% | +12.7% to +37.3% | 1 | 0 | +45.2% | 7 |
| latest print Q4 2012 (2013-02-27 to 2013-04-26) | 9 | +21.6% | +18.3% to +28.4% | 0 | 0 | +39.0% | 9 |
| latest print Q1 2013 (2013-05-02 to 2013-07-26) | 13 | +16.2% | -8.7% to +27.7% | 0 | 0 | +38.5% | 13 |
| latest print Q2 2013 (2013-08-01 to 2013-11-01) | 14 | -11.8% | -22.1% to -7.6% | 0 | 0 | +5.1% | 14 |
| latest print Q3 2013 (2013-11-07 to 2013-12-31) | 9 | -43.8% | -55.1% to -27.6% | 0 | 0 | -21.4% | 9 |
3y (53 dates with one): 1 of 53 cleared, 5 beat SPY; range -37.0% to +53.0%

## What the 2010-2013 labels suggest (hypotheses only)

- **The calls held on 90 of 209 dates:** CHEAP on all 32 (2010-02-24 to 2010-10-01, +72% to +124% over two years, every one clearing the
  hurdle and beating SPY), FAIR on none of 9 (they returned +77% to +113%, as CHEAP would have), RICH on 58 of 168: none of the 11 of 2010,
  5 of the 52 of 2011, 1 of the 52 of 2012, and 52 of the 53 of 2013.
- **The RICH calls of 2010-2012 were wrong for two years and right later.** At 17-29x the guide (the 88th-100th percentile of a 13.5-14.7x
  median), the dates of late 2010 to 2012 returned +15% to +93% over two years, as the multiple kept rising
  (m12-24 average price +14% to +66%; 90 of the 108 ahead of SPY); their three-year horizons turn: no 2012 date cleared the hurdle over three years (-30% to +50%). The
  2013 RICH dates (25-50x, the FY13E after the wind-down charges included) returned -55% to +37% and lagged SPY on all 53 (by 8-70 points),
  the entries from August 2013 losing 8% to 55% with drawdowns of up to -73%. The window of ONEOK's own 2002-2010 earnings marked a
  re-rating that lasted three years as RICH from its start; whether that is early or wrong depends on the horizon, which the two-year check
  fixes.
- **The 2008-2009 hypothesis on BASE is not supported here.** There, BASE on commodity revenues as reported made the late-2009 dates RICH
  against a +91-139% outcome; in 2010 the same reading made 32 dates CHEAP (BASE +26% to +41%/yr on recovering revenues), and all 32 held.
  The sensitivity's net margin reading would have moved 30 of those 32 to FAIR or RICH. One stock, two regimes: the label points both ways.
- **Most dates landed above the BASE scenario** (XBULL 162, BULL 39, BASE 8 at two years, against the model's own scenarios; the 8 BASE
  landings are June 2010 and December 2013).
- **The kind held:** DURABLE then (no 10-K called the business cyclical), DURABLE in today's profile. Label only.
- One stock and four years: "a ten-year own-history window flags a re-rating years before it reverses" is a hypothesis to test on other
  names, not a rule.

# OKE 2014-2017 (hindsight)

Computed after the 2014-2017 build, validation outputs, README section ("OKE 2014-2017") and firewall result were committed and pushed
(`retro_tool.py outcome` on the 209 dates, then `findings_tables.py 2014,2015,2016,2017`). These are labels, never inputs: nothing here
may feed the fact sheet, the builder, the engine or a rule, and changing a rule because of them would need a new method version and a
full re-run with the reason recorded. Every date has a 2-year horizon (the last, 2017-12-29, to 2019-12-27).

**By class (209 dates):** CHEAP 55, median 2-year total return +45.1% (+30.1% to +206.7%), all 55 cleared the 15%/yr hurdle and beat
SPY, the call held on 55; FAIR 42, median +54.0% (+2.0% to +104.9%), 31 cleared, 35 beat SPY, held on 13; RICH 112, median +23.3%
(-58.4% to +80.9%), 43 cleared, 63 beat SPY, held on 49. Legacy tiers: BUY 42 (median +48.5%, 42 cleared), ACCUMULATE 28 (+47.8%, 26),
WATCHLIST 27 (+39.4%, 15), AVOID 112 (+24.8%, 44). The call held on 117 of 209 dates; the price landed in the BULL band on 122, BASE 67,
BEAR 15, XBULL 5.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2014-01-03 to 2014-12-26) | 52 | -24.8% | -58.4% to +38.4% | 1 | 4 | -42.9% | 48 |
| FY13E $1.239 (the Q3 2013 release's $245-275 million) (2014-01-03 to 2014-02-21) | 8 | -49.8% | -58.4% to -45.6% | 0 | 0 | -35.0% | 8 |
| FY14E $1.358 (the 8-K of 2013-12-03's $285 million) (2014-02-26 to 2014-10-31) | 36 | -24.8% | -52.9% to -5.3% | 0 | 0 | -48.3% | 36 |
| FY14E $1.499 (the Q3 2014 release's $316 million) (2014-11-06 to 2014-11-28) | 4 | -1.4% | -7.9% to +6.6% | 0 | 0 | -33.3% | 4 |
| FY14E $1.499 (the 8-K of 2014-12-03's $316 million) (2014-12-05 to 2014-12-26) | 4 | +27.5% | +16.8% to +38.4% | 1 | 4 | -18.5% | 0 |
| latest print Q3 2013 (2014-01-03 to 2014-02-21) | 8 | -49.8% | -58.4% to -45.6% | 0 | 0 | -35.0% | 8 |
| latest print Q4 2013 (2014-02-26 to 2014-05-02) | 10 | -42.0% | -52.9% to -35.4% | 0 | 0 | -42.0% | 10 |
| latest print Q1 2014 (2014-05-08 to 2014-08-01) | 13 | -24.8% | -29.1% to -21.0% | 0 | 0 | -50.2% | 13 |
| latest print Q2 2014 (2014-08-07 to 2014-10-31) | 13 | -19.8% | -25.6% to -5.3% | 0 | 0 | -46.7% | 13 |
| latest print Q3 2014 (2014-11-06 to 2014-12-26) | 8 | +16.8% | -7.9% to +38.4% | 1 | 4 | -26.4% | 4 |

3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -17.4% to +36.0%

1-year total return range -56.9 -3.1 ; 2-year excess over SPY -66.9 21.6

Maximum drawdown within 2 years: -73.3 -62.9

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2015-01-02 to 2015-10-23) | 35 | +33.3% | +19.1% to +65.9% | 18 | 35 | +5.4% | 0 |
| class FAIR, legacy tier WATCHLIST (2015-08-06 to 2015-11-05) | 10 | +72.1% | +62.8% to +84.3% | 10 | 10 | +51.2% | 0 |
| class FAIR, legacy tier ACCUMULATE (2015-11-13 to 2015-11-27) | 3 | +95.8% | +87.4% to +101.4% | 3 | 3 | +88.8% | 0 |
| class CHEAP, legacy tier BUY (2015-12-04 to 2015-12-31) | 5 | +142.1% | +131.7% to +203.9% | 5 | 5 | +122.3% | 5 |
| FY14E $1.499 (the 8-K of 2014-12-03's $316 million) (2015-01-02 to 2015-02-20) | 8 | +33.3% | +22.8% to +42.7% | 4 | 8 | -4.3% | 0 |
| FY15E $1.507 (the Q4 2014 release's $317 million) (2015-02-25 to 2015-12-31) | 45 | +57.9% | +19.1% to +203.9% | 32 | 45 | +37.8% | 5 |
| latest print Q3 2014 (2015-01-02 to 2015-02-20) | 8 | +33.3% | +22.8% to +42.7% | 4 | 8 | -4.3% | 0 |
| latest print Q4 2014 (2015-02-25 to 2015-05-01) | 10 | +25.5% | +19.1% to +31.2% | 0 | 10 | +1.6% | 0 |
| latest print Q1 2015 (2015-05-07 to 2015-07-31) | 13 | +41.2% | +23.0% to +60.8% | 10 | 13 | +29.1% | 0 |
| latest print Q2 2015 (2015-08-06 to 2015-10-30) | 13 | +65.9% | +54.4% to +76.0% | 13 | 13 | +48.5% | 0 |
| latest print Q3 2015 (2015-11-05 to 2015-12-31) | 9 | +131.7% | +84.3% to +203.9% | 9 | 9 | +117.1% | 5 |

3y (53 dates with one): 37 of 53 cleared, 49 beat SPY; range +24.7% to +242.8%

1-year total return range -52.2 221.6 ; 2-year excess over SPY 1.6 165.2

Maximum drawdown within 2 years: -62.9 -23.2

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2016-01-08 to 2016-04-01) | 11 | +160.2% | +116.5% to +206.7% | 11 | 11 | +115.4% | 11 |
| class CHEAP, legacy tier ACCUMULATE (2016-02-05 to 2016-11-03) | 3 | +106.8% | +47.5% to +138.4% | 3 | 3 | +80.5% | 3 |
| class FAIR, legacy tier ACCUMULATE (2016-03-18 to 2016-11-18) | 4 | +101.6% | +35.2% to +104.9% | 4 | 4 | +71.1% | 2 |
| class FAIR, legacy tier WATCHLIST (2016-04-22 to 2016-12-30) | 7 | +21.1% | +2.0% to +81.2% | 2 | 2 | +14.8% | 5 |
| class RICH, legacy tier WATCHLIST (2016-04-29 to 2016-12-16) | 2 | +80.9% | +13.2% to +80.9% | 1 | 1 | +50.5% | 1 |
| class FAIR, legacy tier AVOID (2016-05-13 to 2016-05-20) | 2 | +73.8% | +70.8% to +73.8% | 2 | 2 | +33.8% | 0 |
| class RICH, legacy tier AVOID (2016-05-27 to 2016-10-28) | 23 | +58.4% | +41.1% to +68.9% | 23 | 23 | +24.3% | 0 |
| FY15E $1.507 (the Q4 2014 release's $317 million) (2016-01-08 to 2016-02-19) | 7 | +168.2% | +138.4% to +206.7% | 7 | 7 | +132.1% | 7 |
| FY16E $1.71 (the 8-K of 2015-12-22's $360 million) (2016-02-24 to 2016-07-29) | 23 | +73.8% | +58.4% to +194.4% | 23 | 23 | +33.8% | 6 |
| FY16E $1.693 (the Q2 2016 release's $360 million) (2016-08-04 to 2016-12-30) | 22 | +45.2% | +2.0% to +62.7% | 16 | 16 | +23.8% | 9 |
| latest print Q3 2015 (2016-01-08 to 2016-02-19) | 7 | +168.2% | +138.4% to +206.7% | 7 | 7 | +132.1% | 7 |
| latest print Q4 2015 (2016-02-24 to 2016-04-29) | 10 | +116.5% | +80.9% to +194.4% | 10 | 10 | +88.3% | 6 |
| latest print Q1 2016 (2016-05-05 to 2016-07-29) | 13 | +64.8% | +58.4% to +77.0% | 13 | 13 | +26.6% | 0 |
| latest print Q2 2016 (2016-08-04 to 2016-10-28) | 13 | +48.4% | +41.1% to +62.7% | 13 | 13 | +24.5% | 0 |
| latest print Q3 2016 (2016-11-03 to 2016-12-30) | 9 | +21.1% | +2.0% to +47.5% | 3 | 3 | +14.8% | 9 |

3y (52 dates with one): 46 of 52 cleared, 47 beat SPY; range +41.9% to +273.9%

1-year total return range -6.1 186.3 ; 2-year excess over SPY -12.6 159.5

Maximum drawdown within 2 years: -28.9 -19.7

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST (2017-01-06 to 2017-02-24) | 8 | +26.4% | +8.1% to +39.4% | 2 | 6 | +14.9% | 6 |
| class CHEAP, legacy tier ACCUMULATE (2017-03-01 to 2017-11-17) | 10 | +40.6% | +30.1% to +54.1% | 8 | 10 | +21.8% | 10 |
| class CHEAP, legacy tier BUY (2017-05-04 to 2017-10-27) | 26 | +44.3% | +32.7% to +53.3% | 26 | 26 | +23.5% | 26 |
| class FAIR, legacy tier ACCUMULATE (2017-11-02 to 2017-12-29) | 8 | +53.3% | +45.8% to +54.3% | 8 | 8 | +28.2% | 0 |
| FY16E $1.693 (the Q2 2016 release's $360 million) (2017-01-06 to 2017-02-24) | 8 | +26.4% | +8.1% to +39.4% | 2 | 6 | +14.9% | 6 |
| FY17E $1.67 (the last full year, FY16's $1.67) (2017-03-01 to 2017-07-28) | 22 | +41.4% | +30.1% to +53.3% | 20 | 22 | +25.1% | 22 |
| FY17E $3.341 (the Q2 2017 release's $635-795 million) (2017-08-03 to 2017-10-27) | 13 | +42.6% | +34.8% to +50.6% | 13 | 13 | +20.4% | 13 |
| FY17E $1.865 (the Q3 2017 release's $635-795 million) (2017-11-02 to 2017-12-29) | 9 | +53.3% | +45.8% to +54.3% | 9 | 9 | +28.2% | 1 |
| latest print Q3 2016 (2017-01-06 to 2017-02-24) | 8 | +26.4% | +8.1% to +39.4% | 2 | 6 | +14.9% | 6 |
| latest print Q4 2016 (2017-03-01 to 2017-04-28) | 9 | +38.3% | +30.1% to +42.9% | 7 | 9 | +19.8% | 9 |
| latest print Q1 2017 (2017-05-04 to 2017-07-28) | 13 | +44.5% | +32.7% to +53.3% | 13 | 13 | +28.3% | 13 |
| latest print Q2 2017 (2017-08-03 to 2017-10-27) | 13 | +42.6% | +34.8% to +50.6% | 13 | 13 | +20.4% | 13 |
| latest print Q3 2017 (2017-11-02 to 2017-12-29) | 9 | +53.3% | +45.8% to +54.3% | 9 | 9 | +28.2% | 1 |

3y (52 dates with one): 6 of 52 cleared, 7 beat SPY; range -46.1% to +61.8%

1-year total return range 1.5 48.5 ; 2-year excess over SPY -7.3 30.8

Maximum drawdown within 2 years: -28.9 -28.9

## What the 2014-2017 labels suggest (hypotheses only)

- **2014, RICH on all 52 dates, held on 48** (median 2-year -24.8%, none cleared the hurdle, maximum drawdowns -63% to -73%). The
  classes rested on the separation reaching the guide (FY14E without ONE Gas) before the history and the window did; the labels agree
  with that timing, but the same years include the 2014-2015 commodity collapse, which no 2014 fact sheet could know.
- **2015 to mid-2016, RICH dates did not hold** (2015's 35 RICH dates: median +33.3%, 18 cleared, all beat SPY, held on none; RICH from
  2016-05-27: median +58.4%, all 23 cleared). Those dates sit on BASE read from commodity revenues (-43% to -17%/yr) for a business whose
  FY2016 10-K calls ONEOK Partners' earnings about 88 percent fee-based, and on a window median raised to 27-30x by the seam between the
  restated 2010-2014 and the as-traded prices with ONE Gas. The sensitivity runs (BASE on net margin, 77 classes; the unrestated EPS, 55)
  are where these dates move; reading the labels as a reason to change BASE or the seam would be hindsight entering a rule.
- **CHEAP held everywhere** (18 dates of 2015-12-04 to 2016-04-08 at 12.6-17.5x after the price fell to $19-30, one in November 2016, and 2017 on commodity
  revenue growth),
  the 2016 lows giving the batch's largest returns (+116% to +207%).
- **The merger quarter.** The 13 CHEAP dates on the Q2 2017 range over the quarter's 214.0M shares (FY17E $3.34) held (median +42.6%);
  with the period-end shares 11 of them would have been FAIR, which also cleared. The label favours the mechanical reading here by
  accident; it is no evidence for the share rule.
- **FAIR had the highest median** (+54.0%) but held on only 13 of 42 dates: in this batch FAIR mostly marked prices that went on rising.
- The 3-year lines turn on the 2018-2020 path (2017's dates: 6 of 52 cleared at three years, as the 2020 collapse falls inside them).

# OKE 2018-2021 (hindsight)

Computed after the 2018-2021 build, validation outputs, README section and firewall result were committed and pushed
(`retro_tool.py outcome` on the 209 dates; tables from `python3 retro/generators/oke/findings_tables.py 2018,2019,2020,2021`). These are
labels, never inputs: nothing here may feed `retro/facts/OKE.json`, `retro/build_oke.py`, the engine or a rule. The earlier OKE findings
were not opened in building this batch, and this section was appended without reading them.

Overall: CHEAP 168 dates, median 2-year total return +22.3%, 71 cleared the 15%/yr hurdle, 95 beat SPY, the call held on 95; FAIR 40,
median -19.5%, 8 cleared, 8 beat SPY; RICH 1 (2020-06-05), +64.8%, the call did not hold. Scenario landings: BEAR 92, BASE 86, BULL 31.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST (2018-01-05 to 2018-10-19) | 27 | -46.4% | -52.8% to +48.7% | 7 | 7 | -19.2% | 0 |
| class FAIR, legacy tier ACCUMULATE (2018-02-09 to 2018-02-09) | 1 | +51.5% | +51.5% to +51.5% | 1 | 1 | +29.1% | 0 |
| class CHEAP, legacy tier BUY (2018-02-28 to 2018-12-28) | 17 | -36.3% | -53.2% to +30.8% | 0 | 1 | +7.9% | 1 |
| class CHEAP, legacy tier ACCUMULATE (2018-05-03 to 2018-11-01) | 2 | -42.7% | -44.3% to -42.7% | 0 | 0 | +1.8% | 0 |
| class CHEAP, legacy tier WATCHLIST (2018-05-11 to 2018-10-26) | 5 | -36.4% | -42.1% to -34.3% | 0 | 0 | -6.0% | 0 |
| FY17E $1.865 (the Q3 2017 release's $635-795 million) (2018-01-05 to 2018-02-23) | 8 | +44.8% | +36.0% to +51.5% | 8 | 8 | +21.5% | 0 |
| FY18E $2.752 (the 8-K of 2018-01-24's $955-1,155 million) (2018-02-28 to 2018-04-27) | 9 | -41.0% | -53.2% to +30.8% | 0 | 1 | +19.6% | 1 |
| FY18E $2.56 (the Q1 2018 release's $955-1,155 million) (2018-05-03 to 2018-07-27) | 13 | -41.6% | -52.8% to -19.5% | 0 | 0 | -10.9% | 0 |
| FY18E $2.617 (the Q2 2018 release's $1,020-1,150 million) (2018-08-02 to 2018-10-26) | 13 | -47.7% | -51.3% to -42.1% | 0 | 0 | -24.1% | 0 |
| FY18E $2.844 (the Q3 2018 release's $1,140-1,220 million) (2018-11-01 to 2018-12-28) | 9 | -28.2% | -42.7% to -13.4% | 0 | 0 | -31.3% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-02-23) | 8 | +44.8% | +36.0% to +51.5% | 8 | 8 | +21.5% | 0 |
| latest print Q4 2017 (2018-02-28 to 2018-04-27) | 9 | -41.0% | -53.2% to +30.8% | 0 | 1 | +19.6% | 1 |
| latest print Q1 2018 (2018-05-03 to 2018-07-27) | 13 | -41.6% | -52.8% to -19.5% | 0 | 0 | -10.9% | 0 |
| latest print Q2 2018 (2018-08-02 to 2018-10-26) | 13 | -47.7% | -51.3% to -42.1% | 0 | 0 | -24.1% | 0 |
| latest print Q3 2018 (2018-11-01 to 2018-12-28) | 9 | -28.2% | -42.7% to -13.4% | 0 | 0 | -31.3% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -13.8% to +32.9%
1y range -2.2 49.6 excess 2y -75.8 26.9
drawdown -80.2 -28.9

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2019-01-04 to 2019-06-14) | 9 | -18.6% | -22.1% to -2.5% | 0 | 0 | -41.4% | 0 |
| class CHEAP, legacy tier ACCUMULATE (2019-02-01 to 2019-12-13) | 39 | -10.6% | -27.3% to +5.0% | 0 | 0 | -40.7% | 0 |
| class FAIR, legacy tier ACCUMULATE (2019-09-13 to 2019-12-27) | 4 | -14.9% | -20.2% to -11.6% | 0 | 0 | -29.5% | 0 |
| FY18E $2.844 (the Q3 2018 release's $1,140-1,220 million) (2019-01-04 to 2019-02-22) | 8 | -21.3% | -27.3% to -18.6% | 0 | 0 | -41.7% | 0 |
| FY19E $3.059 (the Q4 2018 release's $1,140-1,400 million) (2019-02-27 to 2019-10-25) | 35 | -11.8% | -20.7% to +5.0% | 0 | 0 | -41.4% | 0 |
| FY19E $3.068 (the Q3 2019 release's $1,220-1,330 million) (2019-10-31 to 2019-12-27) | 9 | -3.1% | -14.9% to +3.1% | 0 | 0 | -28.7% | 0 |
| latest print Q3 2018 (2019-01-04 to 2019-02-22) | 8 | -21.3% | -27.3% to -18.6% | 0 | 0 | -41.7% | 0 |
| latest print Q4 2018 (2019-02-27 to 2019-04-26) | 9 | -17.1% | -20.7% to -12.3% | 0 | 0 | -49.7% | 0 |
| latest print Q1 2019 (2019-05-02 to 2019-07-26) | 13 | -8.6% | -15.9% to -2.5% | 0 | 0 | -42.2% | 0 |
| latest print Q2 2019 (2019-08-01 to 2019-10-25) | 13 | -14.3% | -20.2% to +5.0% | 0 | 0 | -37.8% | 0 |
| latest print Q3 2019 (2019-10-31 to 2019-12-27) | 9 | -3.1% | -14.9% to +3.1% | 0 | 0 | -28.7% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -15.2% to +27.8%
1y range -64.9 41.4 excess 2y -73.6 -48.9
drawdown -80.2 -80.2

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier ACCUMULATE (2020-01-03 to 2020-02-21) | 8 | -9.6% | -12.9% to -6.1% | 0 | 0 | -27.0% | 0 |
| class CHEAP, legacy tier BUY (2020-02-26 to 2020-12-31) | 44 | +124.1% | -2.5% to +280.9% | 42 | 42 | +103.8% | 42 |
| class RICH, legacy tier BUY (2020-06-05 to 2020-06-05) | 1 | +64.8% | +64.8% to +64.8% | 1 | 1 | +34.1% | 0 |
| FY19E $3.068 (the Q3 2019 release's $1,220-1,330 million) (2020-01-03 to 2020-02-21) | 8 | -9.6% | -12.9% to -6.1% | 0 | 0 | -27.0% | 0 |
| FY20E $3.55 (the Q4 2019 release's $3.25-3.85) (2020-02-26 to 2020-04-24) | 9 | +174.1% | -2.5% to +280.9% | 7 | 7 | +106.7% | 7 |
| FY20E $1.685 (the Q1 2020 release's $500-900 million) (2020-04-30 to 2020-10-23) | 26 | +124.1% | +64.8% to +165.7% | 26 | 26 | +111.3% | 25 |
| FY20E $1.571 (the Q3 2020 release's $500-900 million) (2020-10-29 to 2020-12-31) | 10 | +95.8% | +70.9% to +153.7% | 10 | 10 | +66.2% | 10 |
| latest print Q3 2019 (2020-01-03 to 2020-02-21) | 8 | -9.6% | -12.9% to -6.1% | 0 | 0 | -27.0% | 0 |
| latest print Q4 2019 (2020-02-26 to 2020-04-24) | 9 | +174.1% | -2.5% to +280.9% | 7 | 7 | +106.7% | 7 |
| latest print Q1 2020 (2020-04-30 to 2020-07-24) | 13 | +111.9% | +64.8% to +140.6% | 13 | 13 | +90.1% | 12 |
| latest print Q2 2020 (2020-07-30 to 2020-10-23) | 13 | +140.9% | +109.8% to +165.7% | 13 | 13 | +121.5% | 13 |
| latest print Q3 2020 (2020-10-29 to 2020-12-31) | 10 | +95.8% | +70.9% to +153.7% | 10 | 10 | +66.2% | 10 |
3y (53 dates with one): 43 of 53 cleared, 43 beat SPY; range -1.9% to +252.6%
1y range -45.0 162.3 excess 2y -63.6 197.7
drawdown -80.2 -27.6

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2021-01-08 to 2021-12-31) | 52 | +34.6% | +13.2% to +90.2% | 29 | 52 | +17.4% | 52 |
| FY20E $1.571 (the Q3 2020 release's $500-900 million) (2021-01-08 to 2021-02-19) | 7 | +77.5% | +63.2% to +90.2% | 7 | 7 | +46.6% | 7 |
| FY21E $2.74 (the Q4 2020 release's $2.40-3.08) (2021-02-24 to 2021-04-23) | 9 | +43.7% | +30.9% to +60.7% | 8 | 9 | +23.4% | 9 |
| FY21E $3.02 (the Q1 2021 release's $2.69-3.35) (2021-04-29 to 2021-07-30) | 14 | +29.1% | +15.3% to +42.0% | 5 | 14 | +17.4% | 14 |
| FY21E $3.021 (the Q2 2021 release's $1,200-1,500 million) (2021-08-05 to 2021-10-29) | 13 | +34.6% | +13.2% to +45.0% | 7 | 13 | +14.8% | 13 |
| FY21E $3.33 (the Q3 2021 release's $3.33) (2021-11-04 to 2021-12-31) | 9 | +22.3% | +14.0% to +34.0% | 2 | 9 | +5.5% | 9 |
| latest print Q3 2020 (2021-01-08 to 2021-02-19) | 7 | +77.5% | +63.2% to +90.2% | 7 | 7 | +46.6% | 7 |
| latest print Q4 2020 (2021-02-24 to 2021-04-23) | 9 | +43.7% | +30.9% to +60.7% | 8 | 9 | +23.4% | 9 |
| latest print Q1 2021 (2021-04-29 to 2021-07-30) | 14 | +29.1% | +15.3% to +42.0% | 5 | 14 | +17.4% | 14 |
| latest print Q2 2021 (2021-08-05 to 2021-10-29) | 13 | +34.6% | +13.2% to +45.0% | 7 | 13 | +14.8% | 13 |
| latest print Q3 2021 (2021-11-04 to 2021-12-31) | 9 | +22.3% | +14.0% to +34.0% | 2 | 9 | +5.5% | 9 |
3y (52 dates with one): 52 of 52 cleared, 52 beat SPY; range +63.1% to +106.8%
1y range -11.2 65.8 excess 2y 10.8 80.5
drawdown -31.3 -31.3

## What the 2018-2021 labels suggest (hypotheses only)

- The class sorted the four years badly at first and well later. The CHEAP dates of 2018-2019 (72 of them) lost 9-53% over two years,
  every one into the March 2020 collapse (drawdowns to -80%); the CHEAP dates from 2020-02-26 on (96) gained +13% to +281%, and the call
  held on 94 of them. The 2018-2019 CHEAP calls priced the merged company's guided earnings at 20-25x against a window median of 32x
  built on the smaller pre-merger earnings: a cheapness that came from the window's composition more than from the price.
- The FAIR dates of early 2018 (FY17E on the Q3 2017 range) gained +36% to +52% over two years, the only FAIR group to clear the hurdle;
  the FAIR dates later in 2018 and in late 2019 lost 6% to 53%.
- The guides did not anticipate 2020: FY20E $3.55 (February 2020) sat beside a -80% drawdown within weeks, and the withdrawn-and-replaced
  outlook ($500-900M) is what the CHEAP calls of April-December 2020 rested on. The sensitivity shows the outlook itself moved only one
  class; the window and the guides carried the result.
- BEAR was the most frequent landing (92 of 209), mostly the 2018-2019 dates: the scenario floor (the worst year of the decade) was not
  too pessimistic for a two-year horizon that contained 2020.
- None of this justifies a rule change: reading the merger as a break in the window, or discounting guides in a commodity downturn,
  would be rules fitted to this outcome and would need a new method version, a full re-run and a recorded reason.
