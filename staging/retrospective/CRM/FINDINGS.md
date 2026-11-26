# CRM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CRM weekly dates: 262, 105 from 2008-01-04 to 2009-12-31 and 157 from 2010-01-08 to 2012-12-31,
all salesforce.com, inc. (NYSE: CRM). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The
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
