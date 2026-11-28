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

