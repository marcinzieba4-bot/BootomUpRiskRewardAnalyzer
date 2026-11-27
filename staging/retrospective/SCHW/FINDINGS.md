# SCHW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SCHW weekly dates: 105, from 2008-01-04 to 2009-12-31, all The Charles Schwab Corporation
(Nasdaq: SCHW). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after
its point-in-time build, validation outputs, README section and firewall result were committed and pushed (076c155, 8c17cc4, 0f13269,
601f677); the outcomes were computed on 2026-11-27. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31).
Total returns include dividends; no split falls in any horizon, so every price is as traded. Medians of an even count take the upper
middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY). Every date was CHEAP and legacy tier BUY, so these tables test
one call against the calendar and the inputs it rested on.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2008-01-04 to 2008-12-31) | 53 | -15.3% | -43.7% to +14.9% | 0 | 16 | -15.0% | 16 |
| FY07E $0.69 (FY06's) (2008-01-04 to 2008-01-11) | 2 | -13.2% | -15.5% to -13.2% | 0 | 2 | -24.5% | 2 |
| FY08E $0.92 (FY07's) (2008-01-17 to 2008-12-31) | 51 | -15.3% | -43.7% to +14.9% | 0 | 14 | -14.6% | 14 |
| latest print Q3 2007 (2008-01-04 to 2008-01-11) | 2 | -13.2% | -15.5% to -13.2% | 0 | 2 | -24.5% | 2 |
| latest print Q4 2007 (2008-01-17 to 2008-04-11) | 13 | -4.3% | -14.2% to +7.5% | 0 | 12 | -10.1% | 12 |
| latest print Q1 2008 (2008-04-16 to 2008-07-11) | 13 | -22.9% | -29.1% to -3.2% | 0 | 2 | -15.6% | 2 |
| latest print Q2 2008 (2008-07-17 to 2008-10-10) | 13 | -35.3% | -43.7% to -27.3% | 0 | 0 | -24.0% | 0 |
| latest print Q3 2008 (2008-10-16 to 2008-12-31) | 12 | -5.8% | -28.2% to +14.9% | 0 | 0 | -0.4% | 0 |

- **CHEAP held on 16 of the 53 dates of 2008, all on the benchmark and none on the hurdle.** The entries of 2008-01-04 to 2008-04-25
  (but 2008-01-17) returned -15.5% to +7.5% over two years and beat SPY by 0.8 to 14.3pp, SPY's own two-year return being negative on each of
  those dates. From 2008-05-02 every entry lagged SPY (by 0.1 to 64.1pp); those after the Q2 2008 print ($20.20-25.25,
  July to early October 2008) returned -27.3% to -43.7%. Over three years no 2008 entry cleared the hurdle or beat SPY (-49.9% to +4.0%),
  and each sat through a 36-56% drawdown within two years.
- **The current year's EPS was the stale part.** Every 2008 date after the Q4 2007 print read FY08E as FY07's $0.92 (no EPS guide: the
  rollover rule); FY2008 came in at $1.06, so the 2008 multiple was, if anything, overstated. The miss came after: see 2009.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-09 to 2009-12-31) | 52 | -8.5% | -37.8% to +68.5% | 6 | 0 | -8.0% | 6 |
| FY08E $0.92 (FY07's) (2009-01-09 to 2009-01-09) | 1 | +18.8% | +18.8% to +18.8% | 0 | 0 | +6.0% | 0 |
| FY09E $1.06 (FY08's) (2009-01-16 to 2009-12-31) | 51 | -8.6% | -37.8% to +68.5% | 6 | 0 | -8.1% | 6 |
| latest print Q3 2008 (2009-01-09 to 2009-01-09) | 1 | +18.8% | +18.8% to +18.8% | 0 | 0 | +6.0% | 0 |
| latest print Q4 2008 (2009-01-16 to 2009-04-09) | 13 | +31.6% | +11.0% to +68.5% | 6 | 0 | +16.4% | 6 |
| latest print Q1 2009 (2009-04-16 to 2009-07-10) | 13 | +2.4% | -8.7% to +8.8% | 0 | 0 | -8.1% | 0 |
| latest print Q2 2009 (2009-07-17 to 2009-10-09) | 13 | -30.1% | -37.8% to -4.1% | 0 | 0 | -9.4% | 0 |
| latest print Q3 2009 (2009-10-16 to 2009-12-31) | 12 | -32.4% | -37.7% to -23.1% | 0 | 0 | -13.4% | 0 |

- **CHEAP held on 6 of the 52 dates of 2009, all on the hurdle and none on the benchmark.** The entries of 2009-01-30 and 2009-02-13 to
  2009-03-13, around the series low ($11.36 on 2009-03-06), returned +34.4% to +68.5% over two years, yet trailed SPY's rebound by 15.1 to
  41.7pp. Every 2009 entry lagged SPY over two years (by 15.1 to 60.3pp), and from the Q2 2009 print (2009-07-17 on, $16.60-19.49)
  the two-year returns were -4.1% to -37.8%. Over three years no 2009 entry cleared the 52.1% hurdle or beat SPY (-30.0% to +25.8%).
- **What the 2009 dates assumed, and what came:** FY09E stood at FY08's $1.06 on all 51 dates from the Q4 2008 print, with BEAR at -10.3%/yr
  (the history's one down year, FY2003 to FY2004). FY2009 came in at $0.68 (the Q4 2009 release, 2010-01-19, outside the series: net
  revenues $4,193M, -19%, with $224M of money market fund fee waivers) and FY2010 at $0.38 (the Q4 2010 release, 2011-01-18): -36% and
  then -44%. The two-year price landed in the BEAR band on 101 of the 105 dates and in BASE on 4 (2009-04-16 to 2009-05-08); none above.
- **The signals turned, the class did not.** The proxy composite fell from 2.85 (Q3 and Q4 2007) to 1.80 (Q1 and Q2 2009), client assets
  growth sat at BEAR on the Q4 2008 to Q2 2009 prints, and BASE growth went negative from the Q3 2008 print (-0.3% to -15.9%/yr). But the
  price state rests on the multiple of the last full year's EPS against the 2003-2009 P/E history and the EPP floor on that same EPS, so
  in 2009 the price sat 8-46% under a 20x floor on every date and the call stayed CHEAP. The sensitivity run showed the same: only the
  signals at their BEAR values moved classes (13).
  Hypothesis, not a rule: for an earnings stream tied to short-term interest rates and client asset levels (net interest revenue and
  money market fund fees), the rollover rule ("no guide, the last full year stands") overstates the current year after a collapse in
  rates, and a P/E window and EPS history drawn from a rising-rate period (2003-2008 here) set a BEAR case that cannot see a rate-driven
  earnings fall. Test it on other rate-sensitive financials and periods (as a cross-ticker study), never fit it to SCHW.

## Across the series

- `profile_drift` (hindsight): DURABLE, risk 2 on every date; today's 2026 profile in `data/business_profiles.json` also files SCHW
  DURABLE, risk 2 (its one-line "why" was first seen in an outcome output, after every SCHW model had been built, validated and
  committed). It was never an input.
- Where the series sat against its own floors: under the EPP floor on 12 dates of 2008 and all 51 dates from the Q4 2008 print, and under
  the BEAR case (Ratio B negative) on 13 (2008-12-19 to 2009-03-27). The six hurdle hits of 2009 come from inside that last stretch; the
  dates under the floor after it (April to December 2009) returned -37.8% to +8.8% over two years.


# 2010-2013 (hindsight)

209 weekly dates, 2010-01-08 to 2013-12-31. Scored only after the 2010-2013 build, validation outputs, README section and firewall result
were committed and pushed (d13f4cb, a5de2bd, a6e6161, f054550); the outcomes were computed on 2026-11-27, and every date has its four
horizons (the last ends 2016-12-31). The calls are now mixed (CHEAP 90, FAIR 48, RICH 71), so "call held" also tests RICH (it should
miss the hurdle and lag SPY) and FAIR (it should land within 15pp of SPY). Over the batch: CHEAP held on 65 of 90 dates, RICH on 33 of
71, FAIR on none of 48. The two-year price landed in the BULL band on 146 dates, BASE on 61 and BEAR on 2.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2010-01-08 to 2010-10-15) | 17 | -5.4% | -34.7% to +6.8% | 0 | 0 | -10.3% | 0 |
| class RICH, legacy tier WATCHLIST (2010-01-21 to 2010-04-30) | 11 | -23.5% | -30.6% to -15.0% | 0 | 0 | -25.3% | 11 |
| class FAIR, legacy tier WATCHLIST (2010-01-29 to 2010-12-31) | 8 | -17.2% | -33.6% to -13.0% | 0 | 0 | -22.0% | 0 |
| class FAIR, legacy tier ACCUMULATE (2010-05-07 to 2010-12-03) | 8 | -19.0% | -24.5% to -10.7% | 0 | 0 | -19.8% | 0 |
| class CHEAP, legacy tier ACCUMULATE (2010-06-18 to 2010-11-26) | 8 | -11.3% | -16.6% to -7.7% | 0 | 0 | -14.7% | 0 |
| FY09E $1.06 (FY08's) (2010-01-08 to 2010-01-15) | 2 | -33.5% | -34.7% to -33.5% | 0 | 0 | -21.3% | 0 |
| FY10E $0.68 (FY09's) (2010-01-21 to 2010-12-31) | 50 | -15.0% | -33.6% to +6.8% | 0 | 0 | -19.1% | 11 |
| latest print Q3 2009 (2010-01-08 to 2010-01-15) | 2 | -33.5% | -34.7% to -33.5% | 0 | 0 | -21.3% | 0 |
| latest print Q4 2009 (2010-01-21 to 2010-04-09) | 12 | -24.3% | -33.6% to -15.0% | 0 | 0 | -23.3% | 9 |
| latest print Q1 2010 (2010-04-16 to 2010-07-09) | 13 | -20.6% | -28.1% to -3.8% | 0 | 0 | -20.1% | 2 |
| latest print Q2 2010 (2010-07-16 to 2010-10-08) | 13 | -4.0% | -16.6% to +6.8% | 0 | 0 | -9.6% | 0 |
| latest print Q3 2010 (2010-10-15 to 2010-12-31) | 12 | -11.3% | -17.2% to -6.9% | 0 | 0 | -16.4% | 0 |

- **Nothing held but RICH.** No 2010 entry cleared the hurdle or beat SPY over two years (-34.7% to +6.8%, 27.6 to 60.8pp behind it). The
  11 RICH dates of January-April 2010 (on FY09E /bin/bash.68 at 27-29x) returned -30.6% to -15.0% and held; the 25 CHEAP and 16 FAIR dates
  failed. Over three years 22 of the 52 cleared the 52.1% hurdle (-16.8% to +70.1%), the later 2010 entries.
- **What 2010 assumed, and what came:** FY10E stood at FY09's /bin/bash.68 on every date from the Q4 2009 print; FY2010 came in at /bin/bash.38 (the
  YieldPlus, money market fund and credit card charges in) and FY2011 at /bin/bash.70.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST (2011-01-07 to 2011-12-23) | 20 | +87.3% | -16.4% to +126.8% | 18 | 18 | +49.2% | 0 |
| class RICH, legacy tier AVOID (2011-01-19 to 2011-08-05) | 27 | -0.5% | -13.0% to +69.6% | 4 | 5 | -20.8% | 22 |
| class RICH, legacy tier WATCHLIST (2011-07-08 to 2011-07-08) | 1 | +45.3% | +45.3% to +45.3% | 1 | 1 | -0.3% | 0 |
| class CHEAP, legacy tier WATCHLIST (2011-11-18 to 2011-12-30) | 2 | +131.4% | +121.1% to +131.4% | 2 | 2 | +79.1% | 2 |
| class CHEAP, legacy tier ACCUMULATE (2011-11-25 to 2011-12-16) | 2 | +135.7% | +133.6% to +135.7% | 2 | 2 | +82.2% | 2 |
| FY10E $0.68 (FY09's) (2011-01-07 to 2011-01-14) | 2 | -12.0% | -16.4% to -12.0% | 0 | 0 | -25.9% | 0 |
| FY11E $0.38 (FY10's) (2011-01-19 to 2011-12-30) | 50 | +45.6% | -13.0% to +135.7% | 27 | 28 | +4.3% | 26 |
| latest print Q3 2010 (2011-01-07 to 2011-01-14) | 2 | -12.0% | -16.4% to -12.0% | 0 | 0 | -25.9% | 0 |
| latest print Q4 2010 (2011-01-19 to 2011-04-15) | 13 | -6.9% | -13.0% to +3.3% | 0 | 0 | -25.4% | 13 |
| latest print Q1 2011 (2011-04-19 to 2011-07-15) | 13 | +20.3% | -5.6% to +47.8% | 3 | 4 | -11.8% | 9 |
| latest print Q2 2011 (2011-07-19 to 2011-10-14) | 13 | +83.9% | +45.6% to +97.9% | 13 | 13 | +40.6% | 0 |
| latest print Q3 2011 (2011-10-19 to 2011-12-30) | 11 | +116.9% | +82.7% to +135.7% | 11 | 11 | +65.5% | 4 |

- **RICH held on the first half, not on the second.** The 28 RICH dates (January-August 2011, on FY11E /bin/bash.38, FY10's GAAP figure with the
  charges in, at 28-51x) returned -13.0% to +69.6% over two years, 22 of them behind SPY. The FAIR dates of the second half (the price
  falling to 0.77 while the class still read FY10's /bin/bash.38) returned up to +126.8%, so FAIR missed on the upside; the 4 CHEAP dates of
  November-December 2011 returned +121.1% to +135.7%.
- **The batch's largest call sits here.** Read at a derived /bin/bash.65 without the charges, the sensitivity run moves 67 classes, mostly 2011's
  RICH and FAIR toward CHEAP. Hypothesis, not a rule: when the last full year carries large charges that the company reconciles only in
  dollars, the rollover rule's GAAP year can overstate the multiple; test it across tickers whose non-GAAP figures come without a
  per-share line, never fit it to SCHW.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST (2012-01-06 to 2012-01-13) | 2 | +118.4% | +108.1% to +118.4% | 2 | 2 | +69.0% | 0 |
| class CHEAP, legacy tier BUY (2012-01-19 to 2012-12-28) | 50 | +112.2% | +73.2% to +137.8% | 50 | 50 | +91.0% | 50 |
| FY11E $0.38 (FY10's) (2012-01-06 to 2012-01-13) | 2 | +118.4% | +108.1% to +118.4% | 2 | 2 | +69.0% | 0 |
| FY12E $0.70 (FY11's) (2012-01-19 to 2012-12-28) | 50 | +112.2% | +73.2% to +137.8% | 50 | 50 | +91.0% | 50 |
| latest print Q3 2011 (2012-01-06 to 2012-01-13) | 2 | +118.4% | +108.1% to +118.4% | 2 | 2 | +69.0% | 0 |
| latest print Q4 2011 (2012-01-19 to 2012-04-13) | 13 | +94.5% | +73.2% to +118.7% | 13 | 13 | +59.5% | 13 |
| latest print Q1 2012 (2012-04-17 to 2012-07-13) | 13 | +109.1% | +91.0% to +126.1% | 13 | 13 | +91.1% | 13 |
| latest print Q2 2012 (2012-07-18 to 2012-10-12) | 13 | +117.6% | +106.3% to +137.8% | 13 | 13 | +91.0% | 13 |
| latest print Q3 2012 (2012-10-16 to 2012-12-28) | 11 | +117.4% | +95.0% to +129.7% | 11 | 11 | +98.3% | 11 |

- **CHEAP held on all 50 dates of 2012.** On FY12E /bin/bash.70 (FY11's) at 17-22x, the 3rd-34th percentile, the entries returned +73.2% to
  +137.8% over two years and +103.9% to +180.6% over three, all clearing both hurdles and beating SPY (by 37.4 to 95.4pp). FY2012 came in
  at /bin/bash.69, FY2013 at /bin/bash.78 and FY2014 at /bin/bash.95 (the Q4 2013 and Q4 2014 releases, outside the series), and the multiple rose with them.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE (2013-01-04 to 2013-04-05) | 6 | +84.2% | +72.4% to +98.6% | 6 | 6 | +76.7% | 6 |
| class CHEAP, legacy tier WATCHLIST (2013-02-01 to 2013-04-12) | 5 | +75.2% | +58.0% to +80.4% | 5 | 5 | +63.3% | 5 |
| class FAIR, legacy tier WATCHLIST (2013-03-08 to 2013-05-24) | 10 | +75.6% | +63.9% to +82.9% | 10 | 10 | +58.1% | 0 |
| class RICH, legacy tier AVOID (2013-05-31 to 2013-12-31) | 32 | +40.9% | +23.5% to +71.7% | 24 | 32 | +35.9% | 0 |
| FY12E $0.70 (FY11's) (2013-01-04 to 2013-01-11) | 2 | +98.6% | +88.0% to +98.6% | 2 | 2 | +77.9% | 2 |
| FY13E $0.69 (FY12's) (2013-01-17 to 2013-12-31) | 51 | +59.5% | +23.5% to +84.2% | 43 | 51 | +41.3% | 9 |
| latest print Q3 2012 (2013-01-04 to 2013-01-11) | 2 | +98.6% | +88.0% to +98.6% | 2 | 2 | +77.9% | 2 |
| latest print Q4 2012 (2013-01-17 to 2013-04-12) | 13 | +75.2% | +58.0% to +84.2% | 13 | 13 | +63.3% | 9 |
| latest print Q1 2013 (2013-04-16 to 2013-07-12) | 13 | +66.4% | +51.4% to +82.9% | 13 | 13 | +47.3% | 0 |
| latest print Q2 2013 (2013-07-17 to 2013-10-11) | 13 | +45.9% | +30.1% to +68.4% | 11 | 13 | +40.3% | 0 |
| latest print Q3 2013 (2013-10-17 to 2013-12-31) | 12 | +34.1% | +23.5% to +41.5% | 6 | 12 | +25.3% | 0 |

- **CHEAP held, RICH failed.** The 11 CHEAP dates (January to mid-April 2013) returned +58.0% to +98.6%; the 32 RICH dates from
  2013-05-31 (30-38x FY13E /bin/bash.69, the 71st-87th percentile, tier AVOID) returned +23.5% to +71.7% over two years and beat SPY on every
  one (by 1.6 to 38.4pp), 24 of them clearing the hurdle. The year's EPS went from FY12's /bin/bash.69 to /bin/bash.78, /bin/bash.95 and .03 (FY2013-FY2015).

## Across 2008-2013

- Hypothesis, not a rule: the method reads a rate-driven earnings stream with a lag both ways. After the 2008 rate collapse the last full
  year (.06) overstated the earnings to come and the CHEAP calls of 2009 failed; with EPS held down by zero rates, fee waivers and the
  2010 charges, the same own-history P/E made 2011's and 2013's multiples look RICH while the price ran ahead of the recovery the market
  priced. Both rest on the rollover rule (no guide, the last full year stands) and a P/E history drawn from other rate regimes. Test it on
  other rate-sensitive financials as a cross-ticker study (the cross-ticker scripts in `staging/retrospective/`), never inside SCHW's
  archive.
- `profile_drift` (hindsight): DURABLE, risk 2 on every date, as today's 2026 profile.
