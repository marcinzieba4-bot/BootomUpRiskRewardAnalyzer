# CRM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CRM weekly dates: 987, 105 from 2008-01-04 to 2009-12-31, 157 from 2010-01-08 to 2012-12-31,
261 from 2013-01-04 to 2017-12-29, 209 from 2018-01-05 to 2021-12-31 and 255 from 2022-01-07 to 2026-11-20, salesforce.com, inc. (NYSE:
CRM; Salesforce, Inc. from 2022-04-04). The 2022-2026 batch is full data again (the filings themselves: retro/README.md, "CRM
2022-2026"), built in a new session that had not opened this file or any CRM outcome, and scored only after its build, validation
outputs, README section and firewall result were committed and pushed (f70c114, 1d3b63f, 3421949, 3db9626), on 2026-11-27. The 2013-2021 dates are
reduced-data batches (SEC XBRL company facts only, no earnings releases or guidance: retro/README.md, "CRM 2013-2017" and "CRM
2018-2021"). They label a different information set from 2008-2012 and are kept apart below. The 2018-2021 batch was decided in the
session that scored 2013-2017 and was scored only after its build, validation outputs, README section and firewall result were
committed and pushed (0f5faa1, 07a406b, 079ad0f, a0f385c), on 2026-11-27. They were scored only after their build, validation outputs, README section and firewall result were
committed and pushed (a63ef98, 52a4ebe, 3659fb8, 48598de), on 2026-11-27, in a session that had not opened this file or any CRM
outcome before then. They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The
2010-2012 batch was decided in the session that scored 2008-2009 (disclosed in retro/README.md, "CRM 2010-2012") and scored only after
its build, validation outputs, README section and firewall result were committed and pushed (ca1f2e5, 4c7980d, 12109b2, e1c9e54), on
2026-11-26; its 3-year horizons end 2015-12-30, and the four-for-one split of 2013-04-18 falls inside most of them: `outcome.json`
reports every price on the AS_OF share basis (x4 after the split), so the returns are as traded. In 2010-2012 "call held" for RICH
means the date missed the two-year hurdle and lagged SPY.

The 2008-2009 batch was scored only after its point-in-time build, validation outputs, README section and firewall result were committed
and pushed (36669f3, 132ff2d, 200cf2e, 8ba1064); the outcomes were computed on 2026-11-26. Every date has its 6-month, 1-, 2- and 3-year
horizons (the last ends 2012-12-31). salesforce.com paid no dividend in any horizon of the series, so total returns are price returns; no
split falls in a 2008-2009 horizon (the four-for-one split is 2013-04-18), so every price there is as traded. Medians of an even count
take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within 15pp
of it either way. The 8 dates before the Q4 FY08 print were FAIR and the 97 from it CHEAP, every one legacy tier BUY, so these tables test
two calls against the calendar.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2008-02-29 to 2008-12-31) | 45 | +47.0% | +13.8% to +512.6% | 28 | 45 | +10.5% | 45 |
| class FAIR, legacy tier BUY (2008-01-04 to 2008-02-22) | 8 | +27.1% | +20.9% to +35.2% | 2 | 8 | -7.2% | 0 |
| FY08E $0.125 (2008-01-04 to 2008-02-22) | 8 | +27.1% | +20.9% to +35.2% | 2 | 8 | -7.2% | 0 |
| FY09E $0.325 (2008-02-29 to 2008-05-16) | 12 | +29.5% | +13.8% to +36.2% | 1 | 12 | -10.3% | 12 |
| FY09E $0.335 (2008-05-23 to 2008-08-15) | 13 | +32.8% | +19.7% to +56.5% | 7 | 13 | -1.9% | 13 |
| FY09E $0.295 (2008-08-22 to 2008-12-31) | 20 | +296.3% | +99.0% to +512.6% | 20 | 20 | +192.0% | 20 |
| latest print Q3 FY08 (2008-01-04 to 2008-02-22) | 8 | +27.1% | +20.9% to +35.2% | 2 | 8 | -7.2% | 0 |
| latest print Q4 FY08 (2008-02-29 to 2008-05-16) | 12 | +29.5% | +13.8% to +36.2% | 1 | 12 | -10.3% | 12 |
| latest print Q1 FY09 (2008-05-23 to 2008-08-15) | 13 | +32.8% | +19.7% to +56.5% | 7 | 13 | -1.9% | 13 |
| latest print Q2 FY09 (2008-08-22 to 2008-11-14) | 13 | +169.4% | +99.0% to +335.6% | 13 | 13 | +96.9% | 13 |
| latest print Q3 FY09 (2008-11-21 to 2008-12-31) | 7 | +358.3% | +313.1% to +512.6% | 7 | 7 | +201.8% | 7 |

- **CHEAP held on all 45 dates of 2008; FAIR failed on all 8, on the upside.** The January-February 2008 entries ($50.87-58.86, 407-471x
  FY08E $0.125, the 87th-98th percentile) returned +20.9% to +35.2% over two years while SPY fell, +34.9 to +49.9pp ahead of it: a FAIR
  call expects the stock within 15pp of SPY, so each missed by beating it (2 of the 8 cleared the hurdle; over three years all 8 returned
  +130.5% to +178.4%). The robustness block's other reading, RICH, would have missed by more. These entries sat through a 70.5% drawdown
  (the low close $21.96 on 2008-11-19), and the average price of months 12-24 was 3-23% under the entry.
- **The CHEAP dates of February-August 2008 held on the benchmark, not on the hurdle.** On FY09E $0.325 and $0.335 ($55.83-73.10, 172-218x)
  they returned +13.8% to +56.5% over two years, 8 of 25 clearing the hurdle and all 25 beating SPY (by 26.5-64.8pp); the average price of
  months 12-24 was -14.7% to +11.3% from the entry, and each fell 67-71% on the way. Over three years all 25 cleared the 52.1% hurdle
  (+79.5% to +140.9%). From the Q2 FY09 print (FY09E $0.295, $22.32-57.20, 76-194x) the 20 entries returned +99.0% to +512.6% (the best,
  2008-11-21, the series low at 75.7x, its own print's day).
- **The class flipped on a guide, not on the price.** 2008-02-22 ($52.34, FAIR at 419x FY08E $0.125) and 2008-02-29 ($59.72, CHEAP at
  184x FY09E $0.325) are a week and a higher price apart: the Q4 FY08 print moved the current year and its EPS guide, and the stock's
  multiple on it fell from the 89th to the 38th percentile of its own history. FY2010 then came in at $0.63 (the Q4 FY10 release,
  2010-02-24, outside the series; FY2009 was $0.35), so GAAP EPS went from FY2008's $0.15 to $0.63 in two years.
  Hypothesis, not a rule: for a company whose GAAP EPS is a few cents against its revenue (an operating margin of 3-6%, marketing and sales
  at half of revenue, stock-based compensation in), a P/E-percentile call is mostly a call on the next year's EPS level, and an
  own-history window of such years ranks the multiple against EPS that grows fast from a small base. Test it on other tickers and periods
  with small GAAP EPS and fast EPS growth, never fit it to CRM.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-09 to 2009-12-31) | 52 | +235.6% | +34.9% to +449.3% | 52 | 52 | +194.6% | 52 |
| FY09E $0.295 (2009-01-09 to 2009-02-20) | 7 | +394.6% | +351.1% to +449.3% | 7 | 7 | +271.8% | 7 |
| FY10E $0.545 (2009-02-27 to 2009-05-15) | 12 | +259.9% | +222.4% to +395.8% | 12 | 12 | +203.5% | 12 |
| FY10E $0.595 (2009-05-22 to 2009-08-14) | 13 | +267.6% | +184.6% to +320.5% | 13 | 13 | +211.0% | 13 |
| FY10E $0.605 (2009-08-21 to 2009-11-13) | 13 | +112.8% | +96.4% to +145.2% | 13 | 13 | +128.4% | 13 |
| FY10E $0.625 (2009-11-19 to 2009-12-31) | 7 | +65.9% | +34.9% to +95.8% | 7 | 7 | +103.1% | 7 |
| latest print Q3 FY09 (2009-01-09 to 2009-02-20) | 7 | +394.6% | +351.1% to +449.3% | 7 | 7 | +271.8% | 7 |
| latest print Q4 FY09 (2009-02-27 to 2009-05-15) | 12 | +259.9% | +222.4% to +395.8% | 12 | 12 | +203.5% | 12 |
| latest print Q1 FY10 (2009-05-22 to 2009-08-14) | 13 | +267.6% | +184.6% to +320.5% | 13 | 13 | +211.0% | 13 |
| latest print Q2 FY10 (2009-08-21 to 2009-11-13) | 13 | +112.8% | +96.4% to +145.2% | 13 | 13 | +128.4% | 13 |
| latest print Q3 FY10 (2009-11-19 to 2009-12-31) | 7 | +65.9% | +34.9% to +95.8% | 7 | 7 | +103.1% | 7 |

- **CHEAP held on all 52 dates of 2009.** From $26.05-73.77 (88-107x FY09E in January and February, 51-118x FY10E from the Q4 FY09 print)
  the entries returned +34.9% to +449.3% over two years and +113.4% to +412.0% over three, all clearing both hurdles and beating SPY (by
  +18.2 to +369.7pp over two years). The entries of 2009-01-09 to 2009-08-14 (the 1st-17th percentile) returned +184.6% to +449.3%; those
  from the Q2 FY10 print (FY10E $0.605-0.625, 86-118x, the 23rd-38th percentile) +34.9% to +145.2%. FY2010 came
  in at $0.63 against the $0.545-0.625 the models used.
- **The growth signals said BEAR while the stock rose.** Subscription and support growth (+43.7% falling to +21.1%) and deferred revenue
  growth (+37.8% falling to +14.5%) sat under their BASE lines on every print the 2009 dates read (Q3 FY09 to Q3 FY10), lines set by rule
  T at the slowest years of the start-up decade (61% and 68%), and the proxy composite stayed at 1.60-1.75; the price state, not the
  signals, carried the call. Hypothesis, not a rule: rule T over IPO-era years (here +60% to +328% growth) scores a maturing company as
  BEAR on every print and carries no information about its deceleration; test it across the other tickers whose rule-T decade holds
  start-up years (as a cross-ticker study, never inside CRM's archive).
- **Where the two-year price landed:** in the BASE band on 76 of the 105 dates, BEAR on 15 (CHEAP dates of 2008) and BULL on 14; none below
  BEAR or above BULL. `profile_drift` (hindsight): DURABLE, risk 2 on every date; today's 2026 profile files CRM as AI_EXPOSED (GENAI), risk
  3, a judgement made 17 years later and no input here.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2010-01-08 to 2010-05-14) | 19 | +94.4% | +36.3% to +111.4% | 19 | 19 | +74.3% | 19 |
| class FAIR, legacy tier BUY (2010-05-21 to 2010-07-02) | 3 | +69.9% | +59.6% to +79.1% | 3 | 3 | +54.0% | 0 |
| class RICH, legacy tier ACCUMULATE (2010-11-19 to 2010-12-10) | 4 | +9.9% | +6.6% to +10.0% | 0 | 0 | -2.9% | 4 |
| class RICH, legacy tier BUY (2010-06-04 to 2010-12-31) | 26 | +33.7% | +21.4% to +49.3% | 13 | 20 | +25.1% | 5 |
| FY10E $0.625 (2010-01-08 to 2010-02-19) | 7 | +83.5% | +36.3% to +99.9% | 7 | 7 | +98.3% | 7 |
| FY11E $0.59 (2010-02-26 to 2010-05-14) | 12 | +96.6% | +61.2% to +111.4% | 12 | 12 | +71.1% | 12 |
| FY11E $0.39 (2010-05-21 to 2010-08-13) | 13 | +43.1% | +27.2% to +79.1% | 10 | 12 | +43.1% | 1 |
| FY11E $0.44 (2010-08-20 to 2010-11-12) | 13 | +30.9% | +21.4% to +45.1% | 6 | 8 | +18.3% | 4 |
| FY11E $0.465 (2010-11-19 to 2010-12-31) | 7 | +10.0% | +6.6% to +24.7% | 0 | 3 | +0.2% | 4 |
| latest print Q3 FY10 (2010-01-08 to 2010-02-19) | 7 | +83.5% | +36.3% to +99.9% | 7 | 7 | +98.3% | 7 |
| latest print Q4 FY10 (2010-02-26 to 2010-05-14) | 12 | +96.6% | +61.2% to +111.4% | 12 | 12 | +71.1% | 12 |
| latest print Q1 FY11 (2010-05-21 to 2010-08-13) | 13 | +43.1% | +27.2% to +79.1% | 10 | 12 | +43.1% | 1 |
| latest print Q2 FY11 (2010-08-20 to 2010-11-12) | 13 | +30.9% | +21.4% to +45.1% | 6 | 8 | +18.3% | 4 |
| latest print Q3 FY11 (2010-11-19 to 2010-12-31) | 7 | +10.0% | +6.6% to +24.7% | 0 | 3 | +0.2% | 4 |

- **CHEAP held on all 19 dates; FAIR failed on all 3, on the upside.** The CHEAP entries of 2010-01-08 to 2010-05-14 ($62.08-88.16,
  99-149x FY10E $0.625 and FY11E $0.59, the 29th-50th percentile) returned +36.3% to +111.4% over two years and +86.4% to +177.7% over
  three, all clearing both hurdles and beating SPY (by 20.6-84.2pp over two years). The three FAIR dates of May-July 2010 ($83.24-87.11,
  213-223x FY11E $0.39) returned +59.6% to +79.1%, 21.1-53.5pp ahead of SPY, outside FAIR's 15pp band.
- **The class flipped on a guide again, and the price did not follow it.** 2010-05-14 (CHEAP, $84.72, FY11E $0.59) and 2010-05-21
  (FAIR, $83.24, FY11E $0.39 with Jigsaw) are a week and a lower price apart: the Q1 FY11 range took Jigsaw's GAAP effect in, and the
  multiple went from the 50th to the 68th percentile. The two dates returned +61.2% and +79.1% over two years. The mechanism the 2008-2009
  findings describe held (the call moved with the guided GAAP EPS level); the price did not follow that level.
- **RICH held on 9 of the 30 RICH dates of 2010:** five of July-September 2010 ($98.95-119.63, +21.4% to +30.9% over two years, 2.8-10.6pp
  behind SPY) and the four ACCUMULATE dates of 2010-11-19 to 2010-12-10 ($131.61-148.61, 283-320x FY11E $0.465), whose two-year returns
  were +6.6% to +10.0%. The other 21 returned +23.2% to +49.3%; 13 of the 30 cleared the two-year hurdle, 20 beat SPY, and over three years 27 cleared the 52.1% hurdle (+43.5% to +101.1%).

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier BUY (2011-12-23) | 1 | +122.7% | +122.7% to +122.7% | 1 | 1 | +86.4% | 0 |
| class RICH, legacy tier ACCUMULATE (2011-01-07 to 2011-12-09) | 18 | +59.0% | +18.8% to +74.1% | 14 | 15 | +33.2% | 1 |
| class RICH, legacy tier AVOID (2011-02-25 to 2011-05-13) | 12 | +30.3% | +16.9% to +45.4% | 4 | 10 | +15.2% | 2 |
| class RICH, legacy tier BUY (2011-01-21 to 2011-12-30) | 9 | +81.7% | +25.2% to +117.5% | 7 | 9 | +47.8% | 0 |
| class RICH, legacy tier WATCHLIST (2011-05-20 to 2011-10-28) | 12 | +11.8% | -1.9% to +53.8% | 1 | 1 | +8.4% | 11 |
| FY11E $0.465 (2011-01-07 to 2011-02-18) | 7 | +22.3% | +18.8% to +35.3% | 1 | 6 | +5.6% | 1 |
| FY12E $0.095 (2011-02-25 to 2011-05-13) | 12 | +30.3% | +16.9% to +45.4% | 4 | 10 | +15.2% | 2 |
| FY12E loss guide, FY11's $0.47 stands (2011-05-20 to 2011-12-30) | 33 | +55.3% | -1.9% to +122.7% | 22 | 20 | +33.0% | 11 |
| latest print Q3 FY11 (2011-01-07 to 2011-02-18) | 7 | +22.3% | +18.8% to +35.3% | 1 | 6 | +5.6% | 1 |
| latest print Q4 FY11 (2011-02-25 to 2011-05-13) | 12 | +30.3% | +16.9% to +45.4% | 4 | 10 | +15.2% | 2 |
| latest print Q1 FY12 (2011-05-20 to 2011-08-12) | 13 | +11.8% | -1.9% to +35.4% | 2 | 0 | +8.4% | 11 |
| latest print Q2 FY12 (2011-08-19 to 2011-11-11) | 13 | +59.7% | +45.4% to +81.7% | 13 | 13 | +34.5% | 0 |
| latest print Q3 FY12 (2011-11-18 to 2011-12-30) | 7 | +95.8% | +72.4% to +122.7% | 7 | 7 | +69.9% | 0 |

- **RICH held on 14 of 51,** 13 of them among the 15 entries of 2011-04-21 to 2011-07-29 ($132.32-156.67, 297-1,472x, near the 2011
  high close of $159.32 on 2011-07-19), which returned -1.9% to +30.3% over two years as the stock fell to $97.48 on 2012-01-04. From the
  Q2 FY12 print (2011-08-19) no RICH call held: the 19 RICH dates to 2011-12-30 ($101.46-139.14, 216-296x FY11's $0.47) returned +45.4%
  to +117.5%.
- **The FY12E $0.095 dates** (2011-02-25 to 2011-05-13, AVOID, 1,263-1,472x, the 97th-100th percentile) returned +16.9% to +45.4% over
  two years: 4 of 12 cleared the hurdle, 10 beat SPY, and over three years all 12 beat SPY. The highest multiples of the series held 2 of
  12 RICH calls.
- **FAIR failed on its one date, on the upside:** 2011-12-23 ($98.02, the lowest close of the 2011-2012 dates, 209x FY11's $0.47)
  returned +122.7%, 73.2pp ahead of SPY.

## 2012 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier ACCUMULATE (2012-01-27 to 2012-11-09) | 13 | +67.8% | +58.3% to +95.8% | 13 | 13 | +58.0% | 0 |
| class RICH, legacy tier AVOID (2012-03-23 to 2012-04-27) | 6 | +43.0% | +32.7% to +48.2% | 6 | 4 | +29.0% | 0 |
| class RICH, legacy tier BUY (2012-01-06 to 2012-01-20) | 3 | +114.6% | +109.7% to +116.4% | 3 | 3 | +78.5% | 0 |
| class RICH, legacy tier WATCHLIST (2012-02-24 to 2012-12-31) | 31 | +50.2% | +32.1% to +78.0% | 30 | 21 | +44.6% | 1 |
| FY12E loss guide, FY11's $0.47 stands (2012-01-06 to 2012-02-17) | 7 | +95.8% | +88.5% to +116.4% | 7 | 7 | +61.0% | 0 |
| FY13E loss guide, FY11's $0.47 stands (2012-02-24 to 2012-12-31) | 46 | +51.8% | +32.1% to +81.3% | 45 | 34 | +46.3% | 1 |
| latest print Q3 FY12 (2012-01-06 to 2012-02-17) | 7 | +95.8% | +88.5% to +116.4% | 7 | 7 | +61.0% | 0 |
| latest print Q4 FY12 (2012-02-24 to 2012-05-11) | 12 | +46.0% | +32.7% to +78.0% | 12 | 9 | +30.3% | 0 |
| latest print Q1 FY13 (2012-05-18 to 2012-08-17) | 14 | +61.4% | +42.3% to +73.1% | 14 | 11 | +56.0% | 0 |
| latest print Q2 FY13 (2012-08-24 to 2012-11-16) | 13 | +60.0% | +42.9% to +81.3% | 13 | 13 | +48.2% | 0 |
| latest print Q3 FY13 (2012-11-23 to 2012-12-31) | 7 | +46.0% | +32.1% to +51.9% | 6 | 1 | +39.4% | 1 |

- **RICH held on 1 of 53.** Every 2012 entry ($101.06-168.95 as traded, 215-359x FY11's $0.47 with FY13 guided to a loss, the 57th-97th
  percentile) returned +32.1% to +116.4% over two years and +68.4% to +126.4% over three; 52 cleared the two-year hurdle and 41 beat SPY.
  The one that held, 2012-12-14 ($166.81), returned +32.1% against a 32.2% hurdle and lagged SPY by 14.3pp.
- **The AVOID dates** (2012-03-23 to 2012-04-27, 327-339x) returned +32.7% to +48.2%, all 6 clearing the hurdle, 4 beating SPY.

Across the 157 dates of 2010-2012:
- **CHEAP held on 19 of 19, FAIR on 0 of 4 (each by beating SPY by more than 15pp), RICH on 24 of 134.** The RICH dates' two-year returns
  run from -1.9% to +117.5% (median +45.1%); 91 of 134 cleared the two-year hurdle, 96 beat SPY, and over three years 122 cleared the
  52.1% hurdle and 114 beat SPY. The 24 that held returned -1.9% to +32.1%, all entered at the 78th percentile or above.
- **The ordering carried information the class line did not.** Over the 157 dates the rank correlation between the AS_OF P/E percentile
  and the two-year return is -0.64 (-0.56 over three years): the higher the stock sat in its own history, the less it returned. The
  absolute RICH line did not hold, as the window's own median kept rising (149-178x in 2010, 179-196x in 2011-2012). The dates are weekly
  and their horizons overlap, so this is one price path, not 157 observations.
- **A stand-in EPS under guided losses.** On the 86 dates where every guided range was a GAAP loss and FY11's $0.47 stood (2011-05-20 to
  2012-12-31), the class was RICH on 85 and held on 12; the median two-year return was +55.7%. Hypothesis, not a rule: when the current
  year is guided to a GAAP loss while revenue grows 30% or more (here a company whose stock-based compensation and acquisition
  amortization put GAAP income under zero), the last full year's GAAP EPS as a stand-in measures nothing the price follows. Test it on
  other tickers' guided-loss periods with growing revenue, as a cross-ticker study, never fitted to CRM.
- **The growth signals stayed BEAR while growth re-accelerated.** Subscription and support growth rose from +23.0% (Q4 FY10) to +38.7%
  (Q4 FY12) and deferred revenue growth from +18.6% to +47.6%, all under their rule-T BASE lines (61% and 68%), and the proxy composite
  stayed at 1.30-1.75. The 2008-2009 hypothesis holds in the other direction: rule T over IPO-era years registered neither the slowdown
  of 2009 nor the re-acceleration of 2011-2012 (at XBULL the signals move 64 classes, the point-in-time sensitivity in the README).
- **The legacy tiers did not order the returns** (median two-year return: BUY +51.4%, ACCUMULATE +61.4%, WATCHLIST +48.1%, AVOID
  +34.8%); AVOID was the lowest, the other three were not in order.
- **Where the two-year price landed:** in the BASE band on 76 of the 157 dates, BULL on 69 and XBULL on 12 (all RICH); none at BEAR.
  `profile_drift` (hindsight): DURABLE, risk 2 on every date, against today's 2026 AI_EXPOSED (GENAI), risk 3, as before.

## 2013 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2013-01-11 to 2013-12-27) | 43 | +48.9% | +29.0% to +73.7% | 41 | 40 | +30.7% | 1 |
| class RICH, legacy tier WATCHLIST (2013-01-04 to 2013-07-05) | 9 | +80.8% | +33.3% to +95.8% | 9 | 6 | +53.9% | 0 |
| FY2013E loss guide, FY11's $0.47 stands (2013-01-04 to 2013-03-08) | 10 | +39.3% | +29.0% to +52.5% | 9 | 4 | +32.3% | 1 |
| FY2014E: guide not in the sheet, FY11's $0.47 stands (2013-03-12 to 2013-04-12) | 5 | +53.8% | +43.7% to +61.2% | 5 | 5 | +30.7% | 0 |
| FY2014E: guide not in the sheet, FY11's $0.1175 stands (2013-04-19 to 2013-12-27) | 37 | +54.7% | +31.9% to +95.8% | 36 | 37 | +34.6% | 0 |
| latest print Q3 FY13 (2013-01-04 to 2013-03-08) | 10 | +39.3% | +29.0% to +52.5% | 9 | 4 | +32.3% | 1 |
| latest print Q4 FY13 (2013-03-12 to 2013-05-24) | 11 | +61.0% | +43.7% to +73.7% | 11 | 11 | +37.2% | 0 |
| latest print Q1 FY14 (2013-05-29 to 2013-08-30) | 14 | +71.3% | +43.0% to +95.8% | 14 | 14 | +47.9% | 0 |
| latest print Q2 FY14 (2013-09-04 to 2013-11-22) | 12 | +43.1% | +31.9% to +48.1% | 11 | 12 | +25.1% | 0 |
| latest print Q3 FY14 (2013-11-27 to 2013-12-27) | 5 | +50.3% | +42.9% to +52.4% | 5 | 5 | +30.5% | 0 |



- **RICH held on 1 of 52.** Every 2013 entry ($165.42-185.85 as traded before the split, $37.56-57.31 after; 320-488x, the 87th-100th
  percentile) returned +29.0% to +95.8% over two years. 50 cleared the hurdle, 46 beat SPY, and over three years 48 beat SPY. The one
  that held, 2013-02-01, returned +29.0% and lagged SPY by 7.6pp.
- **The WATCHLIST dates returned more than the AVOID dates** (median +80.8% against +48.9%). The five of 2013-06-07 to 2013-07-05 were
  the five lowest entries of the batch ($37.56-39.61) and returned +80.8% to +95.8%.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2014-01-03 to 2014-12-26) | 52 | +29.2% | -5.0% to +59.9% | 23 | 48 | +29.6% | 4 |
| FY2014E: guide not in the sheet, FY11's $0.1175 stands (2014-01-03 to 2014-02-28) | 9 | +12.4% | -5.0% to +42.2% | 1 | 5 | +18.6% | 4 |
| FY2015E: guide not in the sheet, FY11's $0.1175 stands (2014-03-07 to 2014-12-26) | 43 | +32.6% | +13.8% to +59.9% | 22 | 43 | +29.9% | 0 |
| latest print Q3 FY14 (2014-01-03 to 2014-02-28) | 9 | +12.4% | -5.0% to +42.2% | 1 | 5 | +18.6% | 4 |
| latest print Q4 FY14 (2014-03-07 to 2014-05-23) | 12 | +40.3% | +16.1% to +53.0% | 8 | 12 | +37.1% | 0 |
| latest print Q1 FY15 (2014-05-30 to 2014-08-22) | 13 | +49.7% | +29.2% to +59.9% | 12 | 13 | +37.2% | 0 |
| latest print Q2 FY15 (2014-08-28 to 2014-11-21) | 13 | +25.5% | +13.8% to +37.3% | 2 | 13 | +29.7% | 0 |
| latest print Q3 FY15 (2014-11-28 to 2014-12-26) | 5 | +20.3% | +14.9% to +27.8% | 0 | 5 | +25.8% | 0 |



- **RICH held on 4 of 52, the 4 entries of 2014-01-31 to 2014-02-21** ($60.53-63.59, the 100th percentile). They returned -5.0%
  to +12.4% over two years and lagged SPY by 0.8-14.0pp. Three of them are the batch's only negative two-year returns. Over three years
  they returned +28.9% to +30.3%, under the 52.1% hurdle.
- **From the FY2014 10-K** (FY15E, 43 dates) every entry beat SPY over two years (+13.8% to +59.9%), but only 22 cleared the hurdle: the
  RICH call missed on the benchmark rather than on the hurdle.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2015-01-02 to 2015-12-31) | 53 | +27.2% | +15.6% to +43.0% | 13 | 40 | +13.8% | 10 |
| FY2015E: guide not in the sheet, FY11's $0.1175 stands (2015-01-02 to 2015-02-27) | 9 | +28.7% | +15.6% to +39.4% | 3 | 9 | +27.0% | 0 |
| FY2016E: guide not in the sheet, FY11's $0.1175 stands (2015-03-06 to 2015-12-31) | 44 | +25.3% | +16.7% to +43.0% | 10 | 31 | +12.2% | 10 |
| latest print Q3 FY15 (2015-01-02 to 2015-02-27) | 9 | +28.7% | +15.6% to +39.4% | 3 | 9 | +27.0% | 0 |
| latest print Q4 FY15 (2015-03-06 to 2015-05-22) | 12 | +24.0% | +18.1% to +29.4% | 0 | 12 | +14.6% | 0 |
| latest print Q1 FY16 (2015-05-27 to 2015-08-21) | 13 | +23.0% | +16.7% to +32.7% | 1 | 10 | +9.5% | 2 |
| latest print Q2 FY16 (2015-08-26 to 2015-11-20) | 13 | +29.6% | +23.3% to +43.0% | 6 | 8 | +12.2% | 5 |
| latest print Q3 FY16 (2015-11-24 to 2015-12-31) | 6 | +33.3% | +21.6% to +36.4% | 3 | 1 | +15.1% | 3 |



- **RICH held on 10 of 53, the most of any year:** 2015-06-19 to 2015-12-31 ($72.44-82.14, the 97th-100th percentile). They returned
  +16.7% to +31.9% over two years and lagged SPY by 1.7-8.8pp. Over three years every 2015 entry cleared the 52.1% hurdle (51 of 53; +49.0% to
  +128.2%) and all 53 beat SPY. The year's calls held on the two-year horizon only.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2016-01-08 to 2016-12-30) | 52 | +75.9% | +48.7% to +122.9% | 52 | 52 | +38.5% | 0 |
| FY2016E: guide not in the sheet, FY11's $0.1175 stands (2016-01-08 to 2016-03-04) | 9 | +67.3% | +48.7% to +84.0% | 9 | 9 | +36.4% | 0 |
| FY2017E: guide not in the sheet, FY11's $0.1175 stands (2016-03-08 to 2016-12-30) | 43 | +75.9% | +53.6% to +122.9% | 43 | 43 | +40.5% | 0 |
| latest print Q3 FY16 (2016-01-08 to 2016-03-04) | 9 | +67.3% | +48.7% to +84.0% | 9 | 9 | +36.4% | 0 |
| latest print Q4 FY16 (2016-03-08 to 2016-05-20) | 11 | +58.6% | +53.6% to +81.0% | 11 | 11 | +34.0% | 0 |
| latest print Q1 FY17 (2016-05-24 to 2016-08-26) | 14 | +74.8% | +55.6% to +90.3% | 14 | 14 | +36.7% | 0 |
| latest print Q2 FY17 (2016-09-02 to 2016-11-18) | 12 | +102.7% | +70.4% to +122.9% | 12 | 12 | +70.8% | 0 |
| latest print Q3 FY17 (2016-11-23 to 2016-12-30) | 6 | +96.2% | +65.0% to +108.7% | 6 | 6 | +88.6% | 0 |



- **RICH held on 0 of 52.** Every entry ($58.51-82.75, 498-704x FY11's $0.1175, the 80th-100th percentile; Ratio B infinite on 31
  dates to 2016-08-26) returned +48.7% to +122.9% over two years, the best year of the batch. All 52 cleared the hurdle and beat
  SPY. The seven XBULL landings of the batch are all in 2016 (2016-03-08 to 2016-06-17).

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2017-01-06 to 2017-12-29) | 52 | +75.2% | +45.7% to +100.6% | 52 | 52 | +67.3% | 0 |
| FY2017E: guide not in the sheet, FY11's $0.1175 stands (2017-01-06 to 2017-03-03) | 9 | +95.1% | +86.9% to +100.6% | 9 | 9 | +69.2% | 0 |
| FY2018E: guide not in the sheet, FY17's $0.26 stands (2017-03-08 to 2017-12-29) | 43 | +66.2% | +45.7% to +97.9% | 43 | 43 | +64.7% | 0 |
| latest print Q3 FY17 (2017-01-06 to 2017-03-03) | 9 | +95.1% | +86.9% to +100.6% | 9 | 9 | +69.2% | 0 |
| latest print Q4 FY17 (2017-03-08 to 2017-05-19) | 11 | +87.9% | +76.9% to +97.9% | 11 | 11 | +69.1% | 0 |
| latest print Q1 FY18 (2017-05-24 to 2017-08-25) | 14 | +74.8% | +58.5% to +84.8% | 14 | 14 | +67.3% | 0 |
| latest print Q2 FY18 (2017-08-29 to 2017-11-17) | 12 | +55.5% | +45.7% to +66.2% | 12 | 12 | +55.8% | 0 |
| latest print Q3 FY18 (2017-11-24 to 2017-12-29) | 6 | +56.9% | +51.9% to +61.4% | 6 | 6 | +48.3% | 0 |

- **RICH held on 0 of 52.** On FY17's $0.26 from the FY2017 10-K (314-414x, the 88th-99th percentile) the 43 entries returned +45.7%
  to +97.9% over two years. The 9 before it, on FY11's $0.1175, returned +86.9% to +100.6%. All 52 cleared the hurdle and beat SPY.

Across the 261 dates of 2013-2017 (the reduced-data batch):
- **RICH on all 261, held on 15.** The two-year returns run from -5.0% to +122.9% (median +51.5%). 190 cleared the two-year hurdle and
  238 beat SPY; over three years 223 cleared the 52.1% hurdle and 249 beat SPY. The 15 that held are 2013-02-01, 2014-01-31 to
  2014-02-21 and ten dates of June to December 2015. Each returned -5.0% to +31.9% and was entered at the 97th percentile or above.
- **The ordering again carried information the class line did not.** The rank correlation between the AS_OF P/E percentile and the
  two-year return is -0.60 (-0.46 over three years), within a narrow band (80th-100th percentile): the dates at the 100th percentile
  returned least. The dates are weekly and their horizons overlap, so this is one price path, not 261 observations.
- **The stand-in EPS, again.** On the 203 dates where FY11's $0.1175 stood (2013-04-19 to 2017-03-03), the class was RICH on all and
  held on 14; the median two-year return was +44.0%. On the 43 dates of FY17's $0.26 it held on none (+45.7% to +97.9%). This extends
  the 2010-2012 hypothesis (a GAAP stand-in under losses measures nothing the price follows) to the years the reduced data could not
  see guided. Whether a guided EPS would have read differently is not tested: the guides are not in the sheet.
- **The growth signals stayed BEAR.** Subscription and support growth (+22.5% to +36.9%) and deferred revenue growth (+22.8% to +35.4%)
  were under their BEAR lines on every print, and the proxy composite was 1.60-1.75. Rule T over IPO-era years ranked a company growing
  25-37% a year as its worst case, and the composite could not separate the 2014 entries that lost from the 2016 entries that doubled.
- **The legacy tiers:** AVOID on 252 dates (median two-year return +51.5%), WATCHLIST on 9 (+80.8%). Too few WATCHLIST dates to test.
- **Where the two-year price landed:** in the BULL band on 254 of the 261 dates and XBULL on 7 (2016), none at BASE or BEAR. The BULL
  case rested on the decade's EPS CAGR measured across the loss-year gaps.
  `profile_drift` (hindsight): DURABLE, risk 2 on every date, against today's 2026 AI_EXPOSED (GENAI), risk 3, as before.
- **Reduced data, read with care.** These labels score a model that could not see salesforce.com's guidance or 10-K text. Patterns here
  are hypotheses about that information set, and should be retested when the batch is rebuilt from the filings.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2018-01-05 to 2018-12-28) | 52 | +53.7% | +16.6% to +111.1% | 42 | 52 | +29.2% | 0 |
| FY2018E: guide not in the sheet, FY17's $0.26 stands (2018-01-05 to 2018-03-09) | 10 | +63.5% | +18.7% to +73.6% | 9 | 10 | +41.0% | 0 |
| FY2019E: guide not in the sheet, FY18's $0.17 stands (2018-03-13 to 2018-12-28) | 42 | +39.8% | +16.6% to +111.1% | 33 | 42 | +24.5% | 0 |
| latest print Q3 FY18 (2018-01-05 to 2018-03-09) | 10 | +63.5% | +18.7% to +73.6% | 9 | 10 | +41.0% | 0 |
| latest print Q4 FY18 (2018-03-13 to 2018-05-25) | 11 | +29.1% | +16.6% to +39.8% | 4 | 11 | +29.2% | 0 |
| latest print Q1 FY19 (2018-06-01 to 2018-08-31) | 14 | +35.5% | +27.6% to +77.6% | 12 | 14 | +15.6% | 0 |
| latest print Q2 FY19 (2018-09-05 to 2018-11-23) | 12 | +78.6% | +55.1% to +111.1% | 12 | 12 | +31.6% | 0 |
| latest print Q3 FY19 (2018-11-30 to 2018-12-28) | 5 | +67.5% | +61.5% to +84.3% | 5 | 5 | +44.7% | 0 |



- **RICH held on 0 of 52.** Every entry ($106.98-159.03, 411-968x FY17's $0.26 and then FY18's $0.17, the 86th-100th percentile)
  beat SPY over two years (+16.6% to +111.1%, by 11.0-71.1pp) and over three years 51 of 52 did (+61.5% to +138.8%).

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2019-03-08 to 2019-12-27) | 43 | +61.2% | +31.8% to +102.4% | 42 | 31 | +49.7% | 42 |
| class RICH, legacy tier AVOID (2019-01-04 to 2019-03-01) | 9 | +49.4% | +32.2% to +59.7% | 9 | 6 | +31.0% | 0 |
| FY2019E: guide not in the sheet, FY18's $0.17 stands (2019-01-04 to 2019-03-01) | 9 | +49.4% | +32.2% to +59.7% | 9 | 6 | +31.0% | 0 |
| FY2020E: guide not in the sheet, FY19's $1.43 stands (2019-03-08 to 2019-12-27) | 43 | +61.2% | +31.8% to +102.4% | 42 | 31 | +49.7% | 42 |
| latest print Q3 FY19 (2019-01-04 to 2019-03-01) | 9 | +49.4% | +32.2% to +59.7% | 9 | 6 | +31.0% | 0 |
| latest print Q4 FY19 (2019-03-08 to 2019-05-31) | 13 | +38.9% | +31.8% to +57.3% | 12 | 2 | +34.7% | 12 |
| latest print Q1 FY20 (2019-06-07 to 2019-08-23) | 12 | +61.2% | +47.7% to +73.9% | 12 | 11 | +50.5% | 12 |
| latest print Q2 FY20 (2019-08-27 to 2019-11-29) | 14 | +83.3% | +66.1% to +102.4% | 14 | 14 | +54.7% | 14 |
| latest print Q3 FY20 (2019-12-06 to 2019-12-27) | 4 | +63.8% | +50.2% to +64.9% | 4 | 4 | +52.6% | 4 |



- **CHEAP held on 42 of 43** from the FY2019 10-K (2019-03-08), on FY19's $1.43 (100-133x, the 16th-41st percentile). They returned
  +31.8% to +102.4% over two years. The one miss, 2019-03-15, returned +31.8% against the 32.2% hurdle and lagged SPY by 12.7pp.
- **The CHEAP calls held on the two-year horizon only.** Over three years none of the 43 beat SPY or cleared the 52.1% hurdle (-21.9%
  to +39.7%): the horizon ends in 2022, after the 2021 peak.
- **The 9 RICH dates before the 10-K** (FY18's $0.17) returned +32.2% to +59.7%; none held.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2020-01-03 to 2020-02-28) | 9 | +22.5% | +3.9% to +53.7% | 1 | 1 | +36.1% | 1 |
| class RICH, legacy tier AVOID (2020-03-06 to 2020-12-31) | 44 | -11.4% | -46.3% to +58.0% | 4 | 0 | +16.0% | 40 |
| FY2020E: guide not in the sheet, FY19's $1.43 stands (2020-01-03 to 2020-02-28) | 9 | +22.5% | +3.9% to +53.7% | 1 | 1 | +36.1% | 1 |
| FY2021E: guide not in the sheet, FY20's $0.15 stands (2020-03-06 to 2020-12-31) | 44 | -11.4% | -46.3% to +58.0% | 4 | 0 | +16.0% | 40 |
| latest print Q3 FY20 (2020-01-03 to 2020-02-28) | 9 | +22.5% | +3.9% to +53.7% | 1 | 1 | +36.1% | 1 |
| latest print Q4 FY20 (2020-03-06 to 2020-05-29) | 13 | +16.5% | -10.2% to +58.0% | 4 | 0 | +55.0% | 9 |
| latest print Q1 FY21 (2020-06-03 to 2020-08-21) | 12 | -5.4% | -12.7% to +5.7% | 0 | 0 | +20.9% | 12 |
| latest print Q2 FY21 (2020-08-28 to 2020-11-27) | 14 | -39.1% | -46.3% to -29.8% | 0 | 0 | -18.4% | 14 |
| latest print Q3 FY21 (2020-12-04 to 2020-12-31) | 5 | -41.1% | -43.6% to -36.0% | 0 | 0 | -20.4% | 5 |



- **The 9 CHEAP dates of January-February 2020** (FY19's $1.43, $166.17-189.95, the 39th-41st percentile) held on 1. They returned
  +3.9% to +53.7% over two years and lagged SPY on 8, by up to 29.8pp. Over three years all 9 lost (-18.9% to -4.0%).
- **RICH held on 40 of 44 from the FY2020 10-K** (FY20's $0.15, 895-1,807x). The two-year return was -46.3% to +58.0%, median
  -11.4%, and none beat SPY. The entries from the Q2 FY21 10-Q (2020-08-28, $222.42-271.10, the 94th-100th percentile) returned -46.3%
  to -29.8% over two years and lagged SPY by 45.9-58.3pp.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2021-03-19 to 2021-12-31) | 42 | -13.9% | -34.4% to +5.2% | 0 | 2 | -29.4% | 2 |
| class RICH, legacy tier AVOID (2021-01-08 to 2021-03-12) | 10 | -28.4% | -36.7% to -11.5% | 0 | 0 | -22.7% | 10 |
| FY2021E: guide not in the sheet, FY20's $0.15 stands (2021-01-08 to 2021-03-12) | 10 | -28.4% | -36.7% to -11.5% | 0 | 0 | -22.7% | 10 |
| FY2022E: guide not in the sheet, FY21's $4.38 stands (2021-03-19 to 2021-12-31) | 42 | -13.9% | -34.4% to +5.2% | 0 | 2 | -29.4% | 2 |
| latest print Q3 FY21 (2021-01-08 to 2021-03-12) | 10 | -28.4% | -36.7% to -11.5% | 0 | 0 | -22.7% | 10 |
| latest print Q4 FY21 (2021-03-19 to 2021-05-28) | 11 | -9.5% | -16.7% to -5.5% | 0 | 0 | -24.7% | 0 |
| latest print Q1 FY22 (2021-06-03 to 2021-08-20) | 12 | -12.8% | -20.0% to -3.8% | 0 | 0 | -29.6% | 0 |
| latest print Q2 FY22 (2021-08-27 to 2021-11-26) | 14 | -26.3% | -34.4% to -12.6% | 0 | 0 | -33.3% | 0 |
| latest print Q3 FY22 (2021-12-03 to 2021-12-31) | 5 | +3.4% | -5.7% to +5.2% | 0 | 2 | -21.3% | 2 |

- **RICH held on all 10 dates to the FY2021 10-K** (FY20's $0.15), which returned -36.7% to -11.5% over two years.
- **CHEAP held on 2 of 42 from it** (FY21's $4.38, 48-70x, the 11th-31st percentile, the price 13-41% under the EPP floor). They returned
  -34.4% to +5.2% over two years, and none cleared the hurdle. The two that held, 2021-12-23 and 2021-12-31, beat SPY by 1.8pp and 0.7pp.
  Over three years 8 of 42 beat SPY.

Across the 209 dates of 2018-2021 (the second reduced-data batch):
- **CHEAP held on 45 of 94, RICH on 50 of 115.** Every class run is one stand-in year's GAAP EPS, and the run's result follows it:
  - FY17-FY18's $0.26 and $0.17 (RICH): 0 of 61 held;
  - FY19's $1.43 (CHEAP): 43 of 52;
  - FY20's $0.15 (RICH): 50 of 54;
  - FY21's $4.38 (CHEAP): 2 of 42.
- **The P/E-percentile ordering of 2010-2017 did not carry over.** The rank correlation between the AS_OF percentile and the two-year
  return is +0.02, and +0.37 over three years, against -0.60 and -0.46 in 2013-2017. With the stand-in EPS moving from $0.15 to $4.38,
  the percentile ranks the stand-in, not the price. One price path, overlapping horizons.
- **The batch's largest call met its outcome.** The 42 CHEAP dates of 2021 rest on FY2021 at GAAP, $4.38 with $2,170M of investment
  gains and a $1,511M tax benefit. They held on 2. The point-in-time sensitivity (the README) shows the mirror-test reading, FY2021
  excluded, makes all 42 RICH, which would have held on most. Hypothesis, not a rule: a GAAP year lifted by investment gains and a
  tax benefit, used as a stand-in, reads CHEAP when the price does not follow it. Test it across tickers on years whose listed
  one-offs are known, never by excluding FY2021 here after seeing this; changing the encoding needs the releases or a new method version.
- **Where the two-year price landed:** CHEAP dates in the BEAR band on 48 and BASE on 46; RICH dates in BULL on 63, XBULL on 51 and
  BASE on 1.
  `profile_drift` (hindsight): DURABLE, risk 2 on every date, against today's 2026 AI_EXPOSED (GENAI), risk 3, as before.
- **Reduced data, read with care,** as for 2013-2017: these labels score a model without salesforce.com's guidance or 10-K text.


## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY (2022-01-07 to 2022-11-11) | 24 | +40.7% | +10.0% to +117.4% | 16 | 19 | +36.8% | 3 |
| class RICH, legacy tier AVOID (2022-03-03 to 2022-04-08) | 6 | +53.2% | +37.5% to +54.8% | 6 | 6 | +10.1% | 0 |
| class RICH, legacy tier WATCHLIST (2022-04-14 to 2022-04-14) | 1 | +55.6% | +55.6% to +55.6% | 1 | 1 | +25.4% | 0 |
| class RICH, legacy tier ACCUMULATE (2022-04-22 to 2022-05-06) | 3 | +60.0% | +57.0% to +62.7% | 3 | 3 | +39.5% | 0 |
| class FAIR, legacy tier ACCUMULATE (2022-05-13 to 2022-05-27) | 2 | +66.5% | +65.2% to +66.5% | 2 | 2 | +49.4% | 0 |
| class FAIR, legacy tier BUY (2022-05-20 to 2022-11-25) | 11 | +90.1% | +41.4% to +121.9% | 11 | 10 | +75.5% | 1 |
| class CHEAP, legacy tier BUY (2022-12-02 to 2022-12-30) | 5 | +166.1% | +129.8% to +179.4% | 5 | 5 | +113.2% | 5 |
| FY2022E $1.285 (Q3 FY22 release) (2022-01-07 to 2022-02-25) | 8 | +30.3% | +10.0% to +47.2% | 3 | 8 | -2.0% | 0 |
| FY2023E $0.47 (Q4 FY22 release) (2022-03-03 to 2022-05-27) | 13 | +55.6% | +37.5% to +80.1% | 13 | 13 | +25.4% | 0 |
| FY2023E $0.39 (Q1 FY23 release) (2022-06-02 to 2022-08-19) | 12 | +41.0% | +24.6% to +52.6% | 9 | 6 | +38.3% | 4 |
| FY2023E $0.39 (Q2 FY23 release) (2022-08-26 to 2022-11-25) | 14 | +90.1% | +51.6% to +121.9% | 14 | 14 | +73.6% | 0 |
| FY2023E $0.56 (Q3 FY23 release) (2022-12-02 to 2022-12-30) | 5 | +166.1% | +129.8% to +179.4% | 5 | 5 | +113.2% | 5 |
| latest print Q3 FY22 (2022-01-07 to 2022-02-25) | 8 | +30.3% | +10.0% to +47.2% | 3 | 8 | -2.0% | 0 |
| latest print Q4 FY22 (2022-03-03 to 2022-05-27) | 13 | +55.6% | +37.5% to +80.1% | 13 | 13 | +25.4% | 0 |
| latest print Q1 FY23 (2022-06-02 to 2022-08-19) | 12 | +41.0% | +24.6% to +52.6% | 9 | 6 | +38.3% | 4 |
| latest print Q2 FY23 (2022-08-26 to 2022-11-25) | 14 | +90.1% | +51.6% to +121.9% | 14 | 14 | +73.6% | 0 |
| latest print Q3 FY23 (2022-12-02 to 2022-12-30) | 5 | +166.1% | +129.8% to +179.4% | 5 | 5 | +113.2% | 5 |

- **RICH held on 3 of 34, FAIR on 1 of 13.** The RICH dates ($157.73-231.23, 153-488x the GAAP guides: FY22's $1.285, then FY23's
  $0.47 and $0.39) returned +10.0% to +117.4% over two years (median +45.2%); 26 cleared the hurdle and 29 beat SPY. The FAIR dates
  returned +41.4% to +121.9% and beat SPY by more than 15pp on 12. FY2023 came in at GAAP $0.21 and FY2024 at $4.20: the multiples were
  of a GAAP year about to grow twentyfold, which the guided margin step pointed at (BASE up to +61.1%/yr from the Q4 FY22 print) but the class, read off
  the P/E percentile, did not use.
- **CHEAP from the Q3 FY23 print held on all 5** (2022-12-02 to 2022-12-30, $128.27-144.56 on FY23's $0.56), +129.8% to +179.4%.

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2023-01-06 to 2023-12-29) | 52 | +26.2% | -9.4% to +136.4% | 17 | 12 | +38.5% | 17 |
| FY2023E $0.56 (Q3 FY23 release) (2023-01-06 to 2023-02-24) | 8 | +111.9% | +91.1% to +136.4% | 8 | 8 | +78.9% | 8 |
| FY2024E $2.6 (Q4 FY23 release) (2023-03-03 to 2023-05-26) | 13 | +37.7% | +19.7% to +58.5% | 9 | 4 | +44.6% | 9 |
| FY2024E $2.68 (Q1 FY24 release) (2023-06-02 to 2023-08-25) | 13 | +20.9% | +12.7% to +30.2% | 0 | 0 | +35.7% | 0 |
| FY2024E $3.51 (Q2 FY24 release) (2023-09-01 to 2023-11-24) | 13 | +19.9% | +2.4% to +31.4% | 0 | 0 | +36.6% | 0 |
| FY2024E $3.995 (Q3 FY24 release) (2023-12-01 to 2023-12-29) | 5 | +0.6% | -9.4% to +4.6% | 0 | 0 | +4.2% | 0 |
| latest print Q3 FY23 (2023-01-06 to 2023-02-24) | 8 | +111.9% | +91.1% to +136.4% | 8 | 8 | +78.9% | 8 |
| latest print Q4 FY23 (2023-03-03 to 2023-05-26) | 13 | +37.7% | +19.7% to +58.5% | 9 | 4 | +44.6% | 9 |
| latest print Q1 FY24 (2023-06-02 to 2023-08-25) | 13 | +20.9% | +12.7% to +30.2% | 0 | 0 | +35.7% | 0 |
| latest print Q2 FY24 (2023-09-01 to 2023-11-24) | 13 | +19.9% | +2.4% to +31.4% | 0 | 0 | +36.6% | 0 |
| latest print Q3 FY24 (2023-12-01 to 2023-12-29) | 5 | +0.6% | -9.4% to +4.6% | 0 | 0 | +4.2% | 0 |

- **CHEAP held on 17 of 52.** The 8 dates on FY23's $0.56 (January-February) returned +91.1% to +136.4%, and 9 of the 13 on FY24's
  $2.60 (March-May) held (+19.7% to +58.5%). From the Q1 FY24 print (2023-06-02) none held: +2.4% to +31.4% over two years, under the
  hurdle and behind SPY on all 31, as FY24's guide rose from $2.68 to $3.995 and the price with it. Over three years 5 of the 52 beat
  SPY.

## 2024 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2024-01-05 to 2024-11-22) | 47 | -31.4% | -46.2% to +7.6% | 0 | 0 | -16.1% | 0 |
| FY2024E $3.995 (Q3 FY24 release) (2024-01-05 to 2024-02-23) | 8 | -18.0% | -38.0% to +3.3% | 0 | 0 | -5.7% | 0 |
| FY2025E $6.11 (Q4 FY24 release) (2024-03-01 to 2024-05-24) | 13 | -33.8% | -42.8% to -31.4% | 0 | 0 | -17.8% | 0 |
| FY2025E $6.08 (Q1 FY25 release) (2024-05-31 to 2024-08-23) | 13 | -26.9% | -36.9% to -17.1% | 0 | 0 | -13.6% | 0 |
| FY2025E $6.09 (Q2 FY25 release) (2024-08-30 to 2024-11-22) | 13 | -16.7% | -46.2% to +7.6% | 0 | 0 | -27.3% | 0 |
| latest print Q3 FY24 (2024-01-05 to 2024-02-23) | 8 | -18.0% | -38.0% to +3.3% | 0 | 0 | -5.7% | 0 |
| latest print Q4 FY24 (2024-03-01 to 2024-05-24) | 13 | -33.8% | -42.8% to -31.4% | 0 | 0 | -17.8% | 0 |
| latest print Q1 FY25 (2024-05-31 to 2024-08-23) | 13 | -26.9% | -36.9% to -17.1% | 0 | 0 | -13.6% | 0 |
| latest print Q2 FY25 (2024-08-30 to 2024-11-22) | 13 | -16.7% | -46.2% to +7.6% | 0 | 0 | -27.3% | 0 |

- **CHEAP held on 0 of 47 with a two-year horizon.** The entries ($231.94-342.02, 38-73x FY24E and FY25E, the 1st-59th percentile)
  returned -46.2% to +7.6% over two years (median -31.4%), behind SPY by 36.5-80.5pp. The price two years on landed nearest BEAR on
  all 47: the multiple fell as the GAAP EPS rose.

## 2025 (52 dates)

| Group | Dates | Median 1-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2025-01-03 to 2025-11-21) | 47 | -29.5% | -41.5% to +4.1% | 0 | 0 |
| FY2025E $6.175 (Q3 FY25 release) (2025-01-03 to 2025-02-21) | 8 | -31.2% | -41.4% to -17.7% | 0 | 0 |
| FY2026E $6.99 (Q4 FY25 release) (2025-02-28 to 2025-05-23) | 13 | -32.9% | -39.8% to -21.6% | 0 | 0 |
| FY2026E $7.18 (Q1 FY26 release) (2025-05-30 to 2025-08-29) | 14 | -31.8% | -41.5% to +0.6% | 0 | 0 |
| FY2026E $7.01 (Q2 FY26 release) (2025-09-05 to 2025-11-21) | 12 | -3.0% | -19.7% to +4.1% | 0 | 0 |
| latest print Q3 FY25 (2025-01-03 to 2025-02-21) | 8 | -31.2% | -41.4% to -17.7% | 0 | 0 |
| latest print Q4 FY25 (2025-02-28 to 2025-05-23) | 13 | -32.9% | -39.8% to -21.6% | 0 | 0 |
| latest print Q1 FY26 (2025-05-30 to 2025-08-29) | 14 | -31.8% | -41.5% to +0.6% | 0 | 0 |
| latest print Q2 FY26 (2025-09-05 to 2025-11-21) | 12 | -3.0% | -19.7% to +4.1% | 0 | 0 |

- **On one-year returns:** the 47 CHEAP dates with a horizon ($227.11-341.70, 32-55x FY26E) returned -41.5% to +4.1% (median
  -29.5%) and lagged SPY on all, by 14.7-68.0pp. GENAI was on the watch list from 2025-03-07 (text only, company-acknowledged, no
  market read); the 38 dates from then with a one-year horizon returned a median -25.9% and beat SPY on none.

## 2026 (47 dates)

| Group | Dates | Median 6-month total return | Range | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2026-01-02 to 2026-05-22) | 21 | +22.4% | -37.1% to +40.0% | 13 | 14 |
| FY2026E $7.23 (Q3 FY26 release) (2026-01-02 to 2026-02-20) | 8 | -14.5% | -37.1% to +11.4% | 1 | 1 |
| FY2027E $7.89 (Q4 FY26 release) (2026-02-27 to 2026-05-22) | 13 | +28.7% | +0.8% to +40.0% | 12 | 13 |
| latest print Q3 FY26 (2026-01-02 to 2026-02-20) | 8 | -14.5% | -37.1% to +11.4% | 1 | 1 |
| latest print Q4 FY26 (2026-02-27 to 2026-05-22) | 13 | +28.7% | +0.8% to +40.0% | 12 | 13 |

- **On six-month returns only:** the 8 dates on FY26's $7.23 (January-February 2026) returned -37.1% to +11.4%; the 13 from the Q4 FY26
  print, on FY27's $7.89 (the $25 billion accelerated repurchase announced in March), +0.8% to +40.0%, ahead of SPY on all. Twenty-six
  dates have no horizon yet.

Across the 255 dates of 2022-2026 (the first full-data batch since 2012; two-year horizons only on the 151 dates to 2024-11-22):
- **CHEAP held on 22 of 104 with a two-year horizon, RICH on 3 of 34, FAIR on 1 of 13.** The CHEAP calls that held are one run,
  2022-12-02 to 2023-05-19 ($128.27-210.36, the 7th-78th percentile): +34.9% to +179.4% over two years. The 82 from 2023-04-06 to
  2024-11-22 ($192.55-342.02, 38-86x, the 1st-59th percentile) returned -46.2% to +31.8% and lagged SPY on all. Two-year prices of the
  CHEAP dates landed nearest BEAR on 91 of 104. Over three years (99 dates to 2023-11-24) the RICH dates returned +23.3% to +67.9%
  (16 of 34 beat SPY) and the CHEAP dates -25.1% to +106.0% (5 of 52).
- **The own-history anchor was one earlier regime.** With FY2017 and FY2019-FY2023 excluded as distorted, the P/E window held FY2018's
  days (160-232x) and the current year's. From 2023 every date read CHEAP, against that window, as the guided GAAP EPS rose from $2.60
  to $10.23 (the GAAP operating margin from 3% to 20%), and the class was robust to every tested encoding (8 of 8 CHEAP from 2023-03-03).
  It failed from mid-2023 while the multiple fell from 86x to 18x. Hypothesis, not a rule: an own-P/E history drawn from a low-margin
  era, especially one thinned to a single kept year, is no anchor after a margin inflection; robustness to encodings that share the
  window says nothing about the window. Test it on other tickers whose exclusions or inflections left such a window, as a cross-ticker
  study, never fitted to CRM.
- **The ordering ran backwards.** The rank correlation between the AS_OF P/E percentile and the two-year return is +0.53 (+0.41 over
  three years), and between the P/E level and the two-year return +0.79: the highest GAAP multiples (2022, on guides of $0.39-1.285)
  came before the best returns. In 2013-2017 the percentile correlation was -0.60, in 2018-2021 +0.02. One price path, overlapping
  horizons.
- **The pre-outcome tests, scored** (the README's sensitivity, on the dates with a two-year horizon): FY2020 at GAAP would have moved
  47 dates of 2022 to CHEAP, and holds from 4 to 44; every data signal at XBULL 42 dates, 4 to 40; but FY2022 at GAAP 26 dates, 14
  holds to 0; the reduced reading of FY2017 and FY2019-FY2021 34 dates, 14 to 6; FY2021 at GAAP 29, 13 to 8; no margin step 35, 14
  to 8; signals at BEAR 18, 6 to 0; BASE on the latest quarter 9, 0 to 2. The one-off readings cut both ways, each through the window's
  composition in 2022; none touched the 2023-2026 calls. The 2018-2021 hypothesis on FY2021 (a GAAP year lifted by investment gains and
  a tax benefit reads CHEAP when the price does not follow it) is not retested here: this batch excluded FY2021 from the filings'
  listed items, decided without having read it, and FY2021 is no stand-in on any 2022-2026 date.
- **The tiers did not rank the returns:** BUY on 139 dates with a two-year horizon (median +22.3%), AVOID 6 (+53.2%), ACCUMULATE 5
  (+62.7%), WATCHLIST 1. The growth signals stayed under their BEAR lines (subscription and support +8% to +25%, unearned revenue +6% to
  +28%, against rule T's 40% and 43%), as in every batch: the start-up decade's thresholds (the 2008-2009 hypothesis).
- **GENAI.** On the watch list from 2025-03-07, never re-filed, text only. The 2025 CHEAP calls failed while the market derated
  software seats; the ACN re-file test (the P/E at or below the 30th percentile, here on 122 of the 151 dates from 2024) would have
  changed the class label only, not the price state or the call. `profile_drift` (hindsight): DURABLE, risk 2 on every date, against
  today's 2026 AI_EXPOSED (GENAI), risk 3 ("agentic AI compresses per-seat pricing, Agentforce is the counter-bet", reviewed
  2026-09-22).
- **Full data, read with care.** These labels score the full information set again (guides, 10-K text, listed one-offs), unlike
  2013-2021; compare them with the reduced batches only as different information sets.
