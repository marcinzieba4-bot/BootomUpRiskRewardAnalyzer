# BKR retrospective findings (hindsight)

Patterns seen in `outcome.json` for the BKR weekly dates: 497 from 2008-01-04 to 2017-06-30, all Baker Hughes Incorporated (NYSE: BHI).
The 153 dates of 2019-02-01 to 2021-12-31 are a different company (Baker Hughes, a GE company, then Baker Hughes Company) and have their
own section, "2019-2021", with its own notes on dividends and horizons; the 253 dates of 2022-01-07 to 2026-11-06 follow in "2022-2026", where
only 149 have a two-year outcome so far.
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 2b07c92; 2010-2013: 57e05a9; 2014-2017: e026e58). Outcomes were computed on
2026-11-10 from the closes posted to 2026-11-09; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2020-06-30).
Total returns include the $0.13, $0.15 and (from 2014-07-31) $0.17 quarterly dividends, the $17.50 special dividend of the GE combination
(ex-date 2017-07-05) and the later BHGE and BKR dividends; no split falls in a horizon. Medians of an even count take the upper middle
value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`,
always the class's test (a tier row counts the class calls on its dates): CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR
should land within ±15pp of it, and RICH should miss the hurdle and lag it. In 2008-2009 every date is CHEAP and BUY, so the class and the
tier rows coincide.

**Hindsight the model could not see:**
- Baker Hughes confirmed Halliburton's approach on 2014-11-13 (the close rose 19%, from $52.05 to $61.76), agreed a combination on
  2014-11-17 ($67.81), and the agreement ended on 2016-05-01. Two-year endpoints from 2014-11-13 to 2015 and three-year endpoints to 2016-05
  are priced partly by that offer, and so are the 2014-2016 entry prices from November 2014 to April 2016.
- The GE combination was announced on 2016-10-31 and closed on 2017-07-03. Each share then became one BHGE Class A share plus the $17.50
  special dividend, and the price series continues as BHGE's (BKR's from 2019). Endpoints after 2017-07-05 price a different company's
  share; the total return of holding it is still what a Baker Hughes holder got.
- **The m12-24 measure is distorted from mid-2015.** It is a price return without dividends, so for dates whose months 12-24 run past
  2017-07-05 it is understated by the $17.50 special dividend (about 30% of the price). For 2016-2017 it is not a usable measure; the
  2014-2017 sections rank and compare on two-year total return instead.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -33.3% | -55.6% to +107.1% | 13 | 13 | -42.3% | 13 |
| FY06 EPS $4.10 (2008-01-04 to 2008-01-25) | 4 | -36.6% | -46.7% to -32.5% | 0 | 0 | -47.5% | 0 |
| FY07 EPS $4.73 (2008-01-31 to 2008-12-31) | 49 | -31.6% | -55.6% to +107.1% | 13 | 13 | -41.6% | 13 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -36.6% | -46.7% to -32.5% | 0 | 0 | -47.5% | 0 |
| latest print Q4 2007 (2008-01-31 to 2008-04-18) | 12 | -28.4% | -39.7% to -23.3% | 0 | 0 | -41.5% | 0 |
| latest print Q1 2008 (2008-04-23 to 2008-07-18) | 13 | -45.7% | -55.6% to -33.8% | 0 | 0 | -49.7% | 0 |
| latest print Q2 2008 (2008-07-23 to 2008-10-17) | 13 | -39.7% | -50.1% to +39.5% | 2 | 2 | -38.9% | 2 |
| latest print Q3 2008 (2008-10-23 to 2008-12-31) | 11 | +75.2% | +36.3% to +107.1% | 11 | 11 | +44.1% | 11 |

- **CHEAP held on 13 of 53 dates, all from 2008-10-10.** The 40 dates from 2008-01-04 to 2008-10-03 lost 9-56% over two years and
  trailed SPY by 10-38pp (one-year returns -16% to -60%, median -52.7%); the 13 from 2008-10-10 to 2008-12-31 returned +34% to +107% and
  beat SPY by 3-62pp. Over three years only 6 of the 40 early dates beat SPY. Every date sat through a 34-71% drawdown; the low close was
  $26.02 on 2008-12-04.
- **The floor was far above where the stock bottomed.** The EPP floor was 20x the last full year's EPS ($82 in January, $95 from the Q4
  2007 print) on every date, set by a window that holds 1999-2000's trough multiples (calendar-year lows of 208x and 96x); the price sat
  3-71% under it all year, and the stock then fell to 5.5x FY07's $4.73. This is the RCL and MAR pattern of early 2008 (a floor that fell
  with the earnings), here without a guide: the anchor was a record year (FY07, then FY08's $5.30) that 2009 did not repeat. Hypothesis,
  not a rule: for a cyclical without guidance, test a floor on trough-cycle or normalized earnings, and a window whose yearly lows exclude
  years of near-zero EPS, on other tickers and periods; never fit either to BKR's outcomes.
- **The signals read a boom that was still running.** Revenue grew 8-18% a year and North America 7-20% on every print public in 2008; the proxy
  composite was 2.00-2.55 and no signal reached BEAR before the Q1 2009 print. Across the 53 dates the proxy composite ranks the return to
  the m12-24 average price at Spearman +0.38 (the right sign, weakly); the entry price ranks it at -0.94, the EPP gap at -0.98, Ratio B at
  -0.96 and the adjusted gap at +0.35. One stock through one crash mostly tests "buy lower".
- **The two-year price landed nearest BEAR on all 53 dates,** at 0.89-1.35 times the BEAR price and 0.08-0.12 times BULL: BULL's
  +59-76%/yr from 1999's $0.08 was never a reachable case (the AAPL pattern).

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +86.9% | +12.6% to +166.9% | 42 | 52 | +55.0% | 52 |
| FY07 EPS $4.73 (2009-01-09 to 2009-01-23) | 3 | +86.9% | +68.1% to +90.7% | 3 | 3 | +45.7% | 3 |
| FY08 EPS $5.30 (2009-01-29 to 2009-12-31) | 49 | +85.7% | +12.6% to +166.9% | 39 | 49 | +55.1% | 49 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +86.9% | +68.1% to +90.7% | 3 | 3 | +45.7% | 3 |
| latest print Q4 2008 (2009-01-29 to 2009-04-24) | 13 | +130.9% | +89.4% to +166.9% | 13 | 13 | +61.3% | 13 |
| latest print Q1 2009 (2009-04-30 to 2009-07-31) | 14 | +95.6% | +75.7% to +120.9% | 14 | 14 | +50.2% | 14 |
| latest print Q2 2009 (2009-08-06 to 2009-10-30) | 13 | +44.7% | +12.6% to +72.8% | 8 | 13 | +55.1% | 13 |
| latest print Q3 2009 (2009-11-05 to 2009-12-31) | 9 | +31.3% | +16.3% to +43.3% | 4 | 9 | +57.9% | 9 |

- **CHEAP held on all 52 dates by the two-year test,** 42 clearing the hurdle and all beating SPY (by 0.3-75pp); the m12-24 average price
  ran 46-61% (group medians) above the entry. The entries of January to July 2009 ($27-42) returned +68% to +167%.
- **The three-year endpoints tell a different story.** Measured to January-December 2012 ($38-52), the 2009 dates returned -2% to +84%
  (median +21.0%) and beat SPY on only one: the stock gave back much of 2010-2011 by 2012. Read at three years (the +52.1% hurdle or SPY),
  the CHEAP call fails on 44 of 52 dates; eight cleared that hurdle.
- **Right for a reason the model did not see.** The class rested on FY08's $5.30, the last full year, while the 2009 quarters earned
  $0.63, $0.28 and $0.18; the stock rose from 5x that anchor because the cycle turned, not because the anchor was right. Through 2009 the
  proxy composite fell from 2.35 to 1.35 and BASE from +17.0% to -25.1%/yr, yet the price state never moved, as the price stayed 56-75% under
  the floor (20x the last full year: $95, then $106 from the Q4 2008 print). Within the year the entry price ranks the two-year return at Spearman -0.84 and the proxy composite
  at +0.84 (the m12-24 measure: -0.44 and -0.09); the composite's ranking is the calendar, as the later prints were both weaker and
  higher-priced entries.
- **The two-year price landed nearest BEAR on 34 dates and BASE on 18,** at 1.38-2.54 times the BEAR price and 0.11-0.18 times BULL.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 21 | +6.2% | -19.1% to +28.6% | 0 | 0 | +13.3% | 0 |
| class FAIR | 6 | -20.2% | -28.1% to +12.1% | 0 | 0 | -18.3% | 1 |
| class RICH | 25 | -3.3% | -22.0% to +16.7% | 0 | 0 | +21.9% | 25 |
| legacy tier BUY | 12 | -14.1% | -28.1% to +14.0% | 0 | 0 | -9.3% | 0 |
| legacy tier ACCUMULATE | 13 | +17.1% | -4.2% to +28.6% | 0 | 0 | +14.5% | 0 |
| legacy tier WATCHLIST | 5 | +9.3% | +5.0% to +16.7% | 0 | 0 | +39.9% | 4 |
| legacy tier AVOID | 22 | -5.7% | -22.0% to +10.9% | 0 | 0 | +21.7% | 22 |
| latest print Q3 2009, FY08 EPS $5.30 (2010-01-08 to 2010-01-22) | 3 | +11.4% | +4.1% to +14.0% | 0 | 0 | +35.1% | 0 |
| latest print Q4 2009, FY09 EPS $1.36 (2010-01-27 to 2010-04-30) | 14 | -1.2% | -22.0% to +16.7% | 0 | 0 | +26.6% | 14 |
| latest print Q1 2010, FY09 EPS $1.36 (2010-05-05 to 2010-07-30) | 13 | -5.7% | -11.6% to +12.1% | 0 | 0 | +21.7% | 12 |
| latest print Q2 2010, FY09 EPS $1.36 (2010-08-04 to 2010-10-29) | 13 | +17.1% | -4.2% to +28.6% | 0 | 0 | +14.5% | 0 |
| latest print Q3 2010, FY09 EPS $1.36 (2010-11-02 to 2010-12-31) | 9 | -19.1% | -28.1% to -13.2% | 0 | 0 | -16.9% | 0 |

- **RICH held on all 25 of its dates (2010-01-27 to 2010-07-30); CHEAP and FAIR held on 1 of 27.** The RICH dates returned -22% to
  +17% over two years and trailed SPY by 14-43pp, but over one year they returned +38% to +74% and beat SPY by 20-52pp: the call was
  right at the two-year endpoint after a year of being wrong (the m12-24 average price was 1-40% above the entry, at or above the hurdle
  on 4 dates). The stock peaked at $79.94 on 2011-07-25. Over three years no 2010 date beat SPY (median +8.7%).
- **A trough anchor made RICH.** From the Q4 2009 print (2010-01-27) the anchor was FY09's GAAP $1.36, 74% under FY08's $5.30; the
  floor fell from $84.8 to $27.2 (20x) and the price sat 54-99% above it, with BASE at -23.0%/yr (Q4 2009 revenue -23.8%) and then
  -4.0%/yr (Q1 2010). This is 2008 in reverse: there the last full year was a peak and the class CHEAP, here a trough and the class RICH,
  and both times the cycle turned inside the two years.
- **From the Q2 2010 print, CHEAP rested on the BJ Services acquisition.** Revenue as published grew +44.4% (Q2 2010) and +82.7% (Q3
  2010), North America +115% and +181%, against +20.2% and +31.1% in the releases' pro forma combined tables. BASE went to +45.2%/yr and
  then +83.5%/yr and the proxy composite to 2.90 and 3.40. The class turned CHEAP on 2010-08-04 at $42.83, 57% above the floor. Those 18
  CHEAP dates returned -19% to +29% over two years and trailed SPY by 6-38pp; none held. The three January dates, still on FY08's $5.30
  (the price 44-48% under the $84.8 floor), returned +4% to +14% and trailed SPY by 4-14pp.
- **Rankings.** Against the return to the m12-24 average price, the entry price ranks at Spearman -0.54, the EPP gap at -0.64 and the
  proxy composite at -0.73 (the wrong sign: the composite peaked on the acquisition's growth).
- **The two-year price landed nearest BASE on 33 dates, BULL on 10 and BEAR on 9** (the Q3 2010 print's dates, whose $115 BASE was 2.7-2.9
  times the endpoint). From 2010-01-27 BEAR sits at $1-4 (FY09's fall is the worst year), so a BEAR landing means the endpoint was
  under about half of BASE, not that the bear case came true.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 45 | -30.0% | -41.9% to +19.2% | 0 | 0 | -34.8% | 0 |
| class FAIR | 6 | -21.9% | -39.0% to +8.2% | 0 | 0 | -21.8% | 0 |
| class RICH | 1 | -38.3% | -38.3% | 0 | 0 | -43.4% | 1 |
| legacy tier BUY | 32 | -32.5% | -41.9% to +9.0% | 0 | 0 | -37.2% | 0 |
| legacy tier ACCUMULATE | 14 | -2.7% | -21.1% to +19.2% | 0 | 0 | -17.6% | 0 |
| legacy tier WATCHLIST | 5 | +7.1% | -23.7% to +8.3% | 0 | 0 | -16.2% | 0 |
| legacy tier AVOID | 1 | -38.3% | -38.3% | 0 | 0 | -43.4% | 1 |
| latest print Q3 2010, FY09 EPS $1.36 (2011-01-07 to 2011-01-21) | 3 | -22.8% | -27.5% to -21.9% | 0 | 0 | -25.3% | 0 |
| latest print Q4 2010, FY10 EPS $2.06 (2011-01-26 to 2011-04-21) | 13 | -35.2% | -39.9% to -29.1% | 0 | 0 | -38.1% | 0 |
| latest print Q1 2011, FY10 EPS $2.06 (2011-04-28 to 2011-07-22) | 13 | -33.6% | -41.9% to -29.5% | 0 | 0 | -38.7% | 0 |
| latest print Q2 2011, FY10 EPS $2.06 (2011-07-26 to 2011-10-28) | 14 | -9.6% | -38.3% to +9.0% | 0 | 0 | -20.2% | 1 |
| latest print Q3 2011, FY10 EPS $2.06 (2011-11-02 to 2011-12-30) | 9 | +9.0% | +2.3% to +19.2% | 0 | 0 | -5.3% | 0 |

- **One call of 52 held: RICH on 2011-07-26.** No date beat SPY over one, two or three years. Two-year returns ran -42% to +19% and
  trailed SPY by 33-71pp; the three-year median was +0.5%. The stock peaked at $79.94 on 2011-07-25 (the day of the Q2 2011 release) and
  fell to $38.13 on 2012-06-25. Its one RICH date sat at that peak ($79.75); a week later, at $64.54, the class was CHEAP again.
- **CHEAP came from the acquisition's growth again.** From the Q4 2010 print the anchor was FY10's GAAP $2.06 and the floor $39.1 (19x).
  The price sat 17-99% above the floor. BASE took revenue as published:
  - +82.2% (Q4 2010) and +78.2% (Q1 2011), against +31.6% and +23.7% pro forma;
  - +40.5% (Q2 2011), with BJ Services in two of the year-ago quarter's three months;
  - +27.0% (Q3 2011), the first like-for-like quarter.

  BASE ran from +80.5%/yr down to +25.3%/yr, and the proxy composite stayed at 3.20-3.40. The 25 CHEAP dates to 2011-07-22 returned -42%
  to -29% over two years. The 20 CHEAP dates from 2011-08-05, on the partly and then wholly organic comparisons, returned -24% to +19% and
  still trailed SPY by 33-71pp.
- **Rankings.** The entry price ranks the m12-24 return at Spearman -0.99, the EPP gap at -0.87 and the proxy composite at -0.17.
- **The two-year price landed nearest BEAR on 31 dates and BASE on 21.** The BEAR landings are
  2011-01-07 to 2011-09-02, where BASE ($92-155) was 2.0-3.6 times the endpoint.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 52 | +45.9% | +6.5% to +93.7% | 37 | 29 | +33.2% | 37 |
| legacy tier BUY | 49 | +47.0% | +12.5% to +93.7% | 37 | 29 | +33.3% | 37 |
| legacy tier ACCUMULATE | 2 | +12.3% | +11.9% to +12.3% | 0 | 0 | +1.6% | 0 |
| legacy tier WATCHLIST | 1 | +6.5% | +6.5% | 0 | 0 | -5.2% | 0 |
| latest print Q3 2011, FY10 EPS $2.06 (2012-01-06 to 2012-01-20) | 3 | +11.9% | +6.5% to +12.3% | 0 | 0 | -0.6% | 0 |
| latest print Q4 2011, FY11 EPS $4.20 (2012-01-25 to 2012-04-20) | 13 | +31.5% | +12.5% to +71.8% | 6 | 5 | +4.3% | 6 |
| latest print Q1 2012, FY11 EPS $4.20 (2012-04-25 to 2012-07-13) | 12 | +79.2% | +63.4% to +93.7% | 12 | 12 | +40.5% | 12 |
| latest print Q2 2012, FY11 EPS $4.20 (2012-07-20 to 2012-10-12) | 13 | +47.0% | +29.3% to +63.4% | 12 | 11 | +29.9% | 12 |
| latest print Q3 2012, FY11 EPS $4.20 (2012-10-19 to 2012-12-28) | 11 | +36.8% | +21.5% to +60.3% | 7 | 1 | +52.9% | 7 |

- **CHEAP on every date, held on 37 of 52, in four runs:**

  | Dates | Held | Two-year return | Note |
  |---|---|---|---|
  | 2012-01-06 to 2012-03-16 | 1 of 11 | +6.5% to +32.2% | all trailed SPY over one year |
  | 2012-03-23 to 2012-10-05 | 29 of 29 | +35% to +94% | 28 beat SPY |
  | 2012-10-12 to 2012-11-09 | 0 of 5 | +21.5% to +31.5% | trailed SPY by 9-21pp; endpoints 2014-10-10 to 2014-11-07 |
  | 2012-11-16 to 2012-12-28 | 7 of 7 | +35% to +60% | endpoints 2014-11-14 to 2014-12-26 |

  The last two runs differ by their endpoints. The 7 hits' endpoints come after the 19% jump of 2014-11-13 on Halliburton's approach,
  so they rest partly on the offer (hindsight; see the top).
- **A peak anchor again.** From the Q4 2011 print (2012-01-25) the anchor was FY11's adjusted $4.20 and the floor $67.2 (16x). The price
  ($39-52) sat 25-42% under the floor all year. Over the same prints, revenue growth slowed from +21.8% to +3.2%, the proxy composite fell
  from 3.20 to 1.85, and BASE fell from +25.3%/yr to +0.4%/yr. FY12 came in at $3.00, 29% under the anchor: the 2008 pattern, a cyclical
  high the next year did not repeat. The stock still rose from its 2012-06-25 low of $38.13 to $75.35 on 2014-07-02, so the calls of
  March to October 2012 held at two years.
- **At three years the call fails on 37 of 52.** Fifteen dates cleared the +52.1% hurdle and 8 beat SPY; the median was +28.6%, with
  endpoints in 2015.
- **Rankings.** Against the m12-24 return, the entry price ranks at Spearman -0.77, the EPP gap at -0.77 and the proxy composite at -0.80.
  The composite fell through the year as the entries got better.
- **The two-year price landed nearest BASE on 43 dates and BEAR on 9** (2012-01-25 to 2012-03-23, where BASE, $122-126, was 2.0-2.2
  times the endpoint).

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 9 | +40.9% | +30.5% to +57.1% | 7 | 5 | +44.6% | 7 |
| class FAIR | 38 | +24.9% | -15.9% to +50.6% | 15 | 11 | +30.7% | 30 |
| class RICH | 6 | -7.7% | -16.2% to -5.2% | 0 | 0 | +2.0% | 6 |
| legacy tier BUY | 3 | +31.9% | +30.5% to +34.2% | 1 | 0 | +46.6% | 1 |
| legacy tier ACCUMULATE | 28 | +40.9% | +6.6% to +57.1% | 21 | 16 | +38.1% | 26 |
| legacy tier WATCHLIST | 16 | +9.9% | -15.9% to +28.2% | 0 | 0 | +20.2% | 10 |
| legacy tier AVOID | 6 | -7.7% | -16.2% to -5.2% | 0 | 0 | +2.0% | 6 |
| latest print Q3 2012, FY11 EPS $4.20 (2013-01-04 to 2013-01-18) | 3 | +31.9% | +30.5% to +34.2% | 1 | 0 | +46.6% | 1 |
| latest print Q4 2012, FY12 EPS $3.00 (2013-01-24 to 2013-04-12) | 12 | +40.4% | +25.4% to +47.4% | 10 | 5 | +40.3% | 12 |
| latest print Q1 2013, FY12 EPS $3.00 (2013-04-19 to 2013-07-12) | 13 | +41.9% | +24.1% to +57.1% | 11 | 11 | +36.8% | 12 |
| latest print Q2 2013, FY12 EPS $3.00 (2013-07-19 to 2013-10-11) | 13 | +15.0% | +6.6% to +24.9% | 0 | 0 | +27.6% | 12 |
| latest print Q3 2013, FY12 EPS $3.00 (2013-10-18 to 2013-12-31) | 12 | -7.7% | -16.2% to +0.2% | 0 | 0 | +5.3% | 6 |

- **The calls held on 43 of 53.** By class:
  - CHEAP held on 7 of 9, with two-year returns of +30.5% to +57.1%. The 9 dates are the three January dates still on FY11's $4.20 and six
    dates from 2013-01-24 to 2013-06-21 when the price dipped up to 3% under the $45 floor. The two misses are 2013-01-04 and 2013-01-18,
    which trailed SPY.
  - FAIR held on 30 of 38. The misses are 2013-05-03 (+15.4pp over SPY), 2013-08-23 (-16.7pp), and 2013-10-18 and 2013-12-06 to
    2013-12-31 (-20 to -31pp).
  - RICH held on 6 of 6 (2013-10-25 to 2013-11-29), at -16% to -5% over two years, trailing SPY by 25-33pp.
- **The anchor sat near the price.** From the Q4 2012 print (2013-01-24) the anchor was FY12's adjusted $3.00 and the floor $45 (15x).
  The price ($43-58) sat between 3% under and 32% over the floor, with BASE at -5% to +5%/yr and the proxy composite at 1.85 and then 2.20.
  The class turned RICH after the Q3 2013 print, when the price rose to 27-30% over the floor.
- **One year against three.** Over one year the median was +38.6% and 37 dates beat SPY. Over three years the median was +1.6% and no
  date beat SPY; those endpoints fall in 2016. The two-year endpoints (2015-01-02 to 2015-12-30, $43.92-69.02) fall while the Halliburton
  agreement was pending (hindsight; see the top).
- **Rankings.** Against the m12-24 return, the entry price, the EPP gap and Ratio B each rank at Spearman -0.99, the proxy composite at
  -0.73 and the adjusted gap at +0.62. The two-year price landed nearest BASE on all 53 dates.

## Across 2010-2013 (hypotheses, not rules)

- **The anchor moved the class more than the price did.** The last full year's EPS went $5.30, $1.36, $2.06, $4.20, $3.00, and the floor
  $84.8, $27.2, $39.1, $67.2, $45.0, while the weekly price stayed between $38 and $80. Peak anchors gave CHEAP (2008, 2012) and a trough anchor
  gave RICH (early 2010), and the two-year results followed the cycle more than the class. This repeats the 2008-2009 hypothesis: for a
  cyclical without guidance, test an anchor and a floor on normalized or through-cycle earnings, on other tickers and periods, never fitted
  to BKR.
- **As-published acquisition growth.** The CHEAP calls of 2010-08-04 to 2011-07-22 rested on a BASE that counted BJ Services in the
  current quarter and not in the year-ago one. With the releases' pro forma comparisons, the same dates read RICH or FAIR (51 classes).
  The calls would then have held on 46 of 52 dates in 2010 and 27 of 52 in 2011, against 26 and 1 (table below).
  Hypothesis: when an acquisition sits in the current quarter but not the year-ago one, and the company prints a pro forma comparison,
  BASE takes that comparison. Test it on the tickers where the as-published rule was set (PEP, XOM, AVGO) and on others. Never adopt it
  because it scores better on BKR.
- **The proxy composite ranked the outcomes the wrong way in all four years:** -0.73, -0.17, -0.80 and -0.73 against the m12-24 return,
  after +0.38 in 2008 and -0.09 in 2009. Its signals read the latest quarter's growth, which peaked with the stock (Q3 2010 to Q1 2011)
  and fell to its lows with it (2012-2013). The entry price ranked best in every year, at -0.54 to -0.99.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST | 3 | -19.1% | -23.9% to -11.4% | 0 | 0 | +8.5% | 0 |
| class RICH, legacy tier AVOID | 49 | -26.4% | -41.3% to +23.1% | 0 | 6 | -23.9% | 43 |
| latest print Q3 2013, FY12 EPS $3.00 (2014-01-03 to 2014-01-17) | 3 | -19.1% | -23.9% to -11.4% | 0 | 0 | +8.5% | 0 |
| latest print Q4 2013, FY13 EPS $2.62 (2014-01-22 to 2014-04-11) | 12 | -26.8% | -34.8% to -21.1% | 0 | 0 | -11.3% | 12 |
| latest print Q1 2014, FY13 EPS $2.62 (2014-04-17 to 2014-07-11) | 13 | -34.0% | -41.3% to -29.3% | 0 | 0 | -28.4% | 13 |
| latest print Q2 2014, FY13 EPS $2.62 (2014-07-18 to 2014-10-10) | 13 | -24.8% | -38.6% to -3.5% | 0 | 0 | -30.4% | 13 |
| latest print Q3 2014, FY13 EPS $2.62 (2014-10-17 to 2014-12-26) | 11 | +13.9% | -3.7% to +23.1% | 0 | 6 | -13.5% | 5 |

- **RICH held on 43 of 49 dates; the three FAIR dates of January missed.** No 2014 date beat SPY over one year or three. The 40 RICH dates
  to 2014-10-24 returned -41% to 0% over two years and trailed SPY by 14-52pp; the stock fell from a $75.35 high (2014-07-02) to $38.88 on
  2016-01-20. Six of the nine dates from 2014-10-31 to 2014-12-26 missed: they beat SPY by up to 8pp, with endpoints from 2016-10-28 to
  2016-12-23, around the announcement of the GE combination (hindsight; see the top). The three FAIR dates trailed SPY by 27-31pp.
- **Why RICH.** From the Q4 2013 print the anchor was FY13's $2.62 adjusted, a year with Iraq's losses in it, and the floor 16x ($41.92).
  The stock traded at 20.0-28.6x (the 64th-96th percentile), 25-79% over the floor, with BASE at +4.9% to +7.2%/yr: the price sat above
  the two-year BASE value on every date.
- **Rankings.** Against the two-year total return, the entry price ranks at Spearman -0.83, the EPP gap at -0.82 and the proxy composite
  at -0.68.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 3 | +8.6% | -1.4% to +8.9% | 0 | 0 | -12.7% | 0 |
| class FAIR | 10 | -1.9% | -9.0% to +0.9% | 0 | 0 | -16.8% | 1 |
| class RICH | 40 | -3.8% | -13.3% to +18.1% | 0 | 1 | -3.8% | 39 |
| legacy tier ACCUMULATE | 6 | +7.1% | +3.5% to +13.6% | 0 | 0 | +6.6% | 6 |
| legacy tier WATCHLIST | 36 | -3.1% | -11.1% to +8.9% | 0 | 0 | -5.8% | 24 |
| legacy tier AVOID | 11 | -9.9% | -13.3% to +18.1% | 0 | 1 | -13.8% | 10 |
| latest print Q3 2014, FY13 EPS $2.62 (2015-01-02 to 2015-01-16) | 3 | +14.4% | +10.1% to +18.1% | 0 | 1 | -12.5% | 2 |
| latest print Q4 2014, FY14 EPS $4.22 (2015-01-21 to 2015-04-17) | 13 | -1.4% | -9.0% to +8.9% | 0 | 0 | -16.3% | 1 |
| latest print Q1 2015, FY14 EPS $4.22 (2015-04-22 to 2015-07-17) | 13 | -9.9% | -13.3% to -3.1% | 0 | 0 | -13.7% | 13 |
| latest print Q2 2015, FY14 EPS $4.22 (2015-07-22 to 2015-10-16) | 13 | -2.4% | -9.1% to +7.4% | 0 | 0 | -0.2% | 13 |
| latest print Q3 2015, FY14 EPS $4.22 (2015-10-22 to 2015-12-31) | 11 | +1.7% | -6.5% to +13.6% | 0 | 0 | -1.5% | 11 |

- **The CHEAP and FAIR calls on FY14's peak failed; the RICH calls held.** From the Q4 2014 print the anchor was FY14's $4.22, the cycle's high, and
  the floor 13x ($54.86). The 13 dates to the Q1 2015 print (3 CHEAP, 10 FAIR, at 13.7-15.9x) returned -9% to +9% over two years, trailing
  SPY by 7-26pp, and -21% to -37% over one year; one FAIR date held. This is the third peak-anchor CHEAP of the series, after 2008 and
  early 2012.
- **RICH held on 39 of 40.** From the Q1 2015 print BASE took the revenue fall (-22.6%, then -35.9% and -42.2%/yr), and the class read RICH
  though the multiple fell to 9.5-13.8x FY14's EPS and, from August, the price sat under the floor. The 37 RICH dates from 2015-04-22
  returned -13% to +14% over two years and trailed SPY by 23-36pp, with endpoints in 2017 that include the special dividend. The one miss
  is 2015-01-02, which beat SPY.
- **The Halliburton offer stood behind the entries** of the whole year (hindsight): Baker Hughes traded as a target until 2016-04-30.
- **Rankings.** Against the two-year total return, the entry price ranks at Spearman -0.64, the EPP gap at -0.41 and the proxy composite
  at -0.07.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 2 | +40.6% | +28.4% to +40.6% | 1 | 0 | +14.0% | 1 |
| class RICH | 50 | +7.6% | -39.2% to +29.4% | 0 | 0 | -27.4% | 50 |
| legacy tier BUY | 2 | +40.6% | +15.0% to +40.6% | 1 | 0 | +14.0% | 2 |
| legacy tier ACCUMULATE | 12 | +15.5% | +5.5% to +29.4% | 0 | 0 | -5.2% | 11 |
| legacy tier WATCHLIST | 28 | +9.9% | -6.7% to +20.8% | 0 | 0 | -27.7% | 28 |
| legacy tier AVOID | 10 | -33.1% | -39.2% to -15.5% | 0 | 0 | -48.8% | 10 |
| latest print Q3 2015, FY14 EPS $4.22 (2016-01-08 to 2016-01-22) | 3 | +29.4% | +28.4% to +40.6% | 1 | 0 | +10.6% | 2 |
| latest print Q4 2015, FY14 EPS $4.22 (2016-01-29 to 2016-04-22) | 13 | +8.2% | +0.3% to +17.5% | 0 | 0 | -10.5% | 13 |
| latest print Q1 2016, FY14 EPS $4.22 (2016-04-28 to 2016-07-22) | 13 | +16.4% | +9.9% to +22.4% | 0 | 0 | -24.6% | 13 |
| latest print Q2 2016, FY14 EPS $4.22 (2016-07-29 to 2016-10-21) | 13 | +4.2% | -6.7% to +12.1% | 0 | 0 | -34.2% | 13 |
| latest print Q3 2016, FY14 EPS $4.22 (2016-10-26 to 2016-12-30) | 10 | -33.1% | -39.2% to -15.5% | 0 | 0 | -48.8% | 10 |

- **RICH held on all 50 RICH dates, and the year's calls held on 51 of 52.** No date beat SPY over two or three years. The one-year
  returns were strong: 28 dates beat SPY, and the January dates returned +54% to +56% (the 2016-01-20 low was $38.88). Over two years the
  RICH dates returned -39% to +29% and trailed SPY by 14-66pp; the 10 from the Q3 2016 print (at $55-66 after the GE announcement) lost
  15-39%. The two-year endpoints are BHGE's 2018 prices, with the special dividend in the return.
- **Why RICH:** FY14's $4.22 still anchored (2015 and 2016 excluded as losses), at 9.5-15.7x, and BASE was -40.8% to -51.8%/yr on the
  revenue fall, so the two-year BASE value ($17-25) was a fraction of the price. The FAIR dates of 2016-01-08 and 2016-01-15 sat 18-21%
  under the floor at the January low; one held.
- **Rankings.** Against the two-year total return, the entry price and the EPP gap each rank at Spearman -0.85 and the proxy composite at
  -0.14.

## 2017 (26 dates, to 2017-06-30)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 5 | -23.9% | -26.6% to -18.3% | 0 | 0 | -49.6% | 0 |
| class RICH | 21 | -26.3% | -36.1% to -20.6% | 0 | 0 | -51.1% | 21 |
| legacy tier AVOID | 26 | -25.4% | -36.1% to -18.3% | 0 | 0 | -50.6% | 21 |
| latest print Q3 2016, FY14 EPS $4.22 (2017-01-06 to 2017-01-20) | 3 | -31.0% | -36.1% to -30.6% | 0 | 0 | -51.3% | 3 |
| latest print Q4 2016, FY14 EPS $4.22 (2017-01-27 to 2017-04-21) | 13 | -23.8% | -32.8% to -20.6% | 0 | 0 | -50.6% | 13 |
| latest print Q1 2017, FY14 EPS $4.22 (2017-04-26 to 2017-06-30) | 10 | -25.8% | -29.5% to -18.3% | 0 | 0 | -50.4% | 5 |

- **RICH held on all 21; the five FAIR dates (2017-05-26 to 2017-06-30) failed,** at -18% to -27% over two years, 43-47pp behind SPY. Every
  2017 date lost money over one, two and three years (three-year median -35.7%, endpoints in 2020); the stock fell to $20.48 on 2018-12-24.
- **Why FAIR at the end:** Q1 2017's -15.3% revenue lifted BASE to -18.6%/yr and the proxy composite to 2.60, and the price ($54-56) sat 0-10% over
  the floor; the class moved toward FAIR as the business looked to be turning, a turn the share did not follow.
- **Rankings.** Against the two-year total return, the entry price ranks at Spearman -0.60, the EPP gap at -0.57 and the proxy composite
  at +0.24.

## Across 2014-2017 (hypotheses, not rules)

- **RICH held on 153 of 160 dates; CHEAP and FAIR held on 2 of 23.** All 183 calls held on 155. The downturn was read through BASE, the
  latest quarter's revenue growth: from the Q1 2015 print it put the two-year BASE value far under the price, so the class stayed RICH
  while the multiple of FY14's EPS fell to its own lows. The same rule read the 2009 bottom wrongly (BASE -25%/yr, then a doubling) and the
  2010-2011 acquisition growth wrongly. Hypothesis: the latest quarter's revenue growth as a two-year rate is right when a downturn
  persists and wrong at the turn; test a dampened or mean-reverting BASE for cyclicals across tickers, never fitted to BKR.
- **The peak anchor failed a third time.** FY14's $4.22 made early 2015 CHEAP or FAIR (1 of 13 held), as FY07-FY08 made 2008 CHEAP
  (13 of 53) and FY11 made 2012-01-25 to 2012-03-16 CHEAP (1 of 8). This is the strongest pattern of the series and repeats the hypothesis of
  2008-2013: for a cyclical without guidance, test an anchor on normalized or through-cycle earnings.
- **The loss-year rule kept a stale anchor.** With 2015 and 2016 excluded (method r2), FY14's $4.22 anchored to mid-2017, two years after
  the company last earned it; the stock looked 9.5-15x "cheap" on it, and only BASE kept the class RICH. The rule is right that a loss has
  no P/E; what to anchor on after two loss years is open, and an owner question.
- **The entry price ranked the two-year total return best** in every year (-0.60 to -0.85). The proxy composite ranked it -0.68, -0.07,
  -0.14 and +0.24.

## 2019-2021: Baker Hughes, a GE company and Baker Hughes Company (153 dates, 2019-02-01 to 2021-12-31)

A different company from the sections above: the new listing of 2017-07-05 (BHGE; BKR from 2019-10-18), built on its own facts and
engine (retro/README.md, "BKR 2018-2021"). No date from 2017-07-07 to 2019-01-25 exists. Scored only after the point-in-time build was
committed and pushed (e9e8e19) and the firewall had passed at its 20 cutoffs. Outcomes were computed on 2026-11-10; every date has all
four horizons (the last three-year endpoint is 2024-12-30). Dividends are $0.18 a quarter, rising from 2022; no split and no special
dividend falls in a horizon, so the m12-24 measure is usable again. FY18's $0.45 is the EPS anchor on every date.

**Hindsight the model could not see:** the oil-price collapse and COVID-19 (low close $9.33 on 2020-03-23, 60-67% under every 2019
entry), then the recovery to $38.72 on 2022-03-25. Two-year endpoints of 2019 dates fall in 2021, before that recovery was complete;
those of 2020 and 2021 dates fall in 2022 and 2023.

### 2019 (48 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 48 | +3.1% | -18.4% to +28.6% | 0 | 0 | -15.3% | 0 |
| latest print Q4 2018 (2019-02-01 to 2019-04-26) | 13 | -11.4% | -18.4% to +0.2% | 0 | 0 | -35.0% | 0 |
| latest print Q1 2019 (2019-05-01 to 2019-07-26) | 13 | +1.8% | -10.5% to +21.1% | 0 | 0 | -18.9% | 0 |
| latest print Q2 2019 (2019-08-01 to 2019-10-25) | 13 | +10.0% | -10.2% to +28.6% | 0 | 0 | -5.3% | 0 |
| latest print Q3 2019 (2019-10-31 to 2019-12-27) | 9 | +11.4% | -2.3% to +23.9% | 0 | 0 | +1.8% | 0 |

- **CHEAP and BUY on all 48 dates, with robustness 8 of 8, and it held on none.** No date cleared the hurdle or beat SPY over two years
  (25-64pp behind, median -46.6pp); one-year returns were -60.5% to +1.4% (median -32.1%) and every date sat through a 64-67% drawdown.
  Over three years 6 cleared the hurdle and 14 beat SPY (median +30.9%). Every two-year endpoint landed nearest the BEAR price.
- **Why CHEAP:** 46-62x one year's $0.45 looked low only against the same stock's 2018 range (median 58-71x), with BASE at +8% to +17%/yr
  from as-reported revenue growth and a 2018 buyback read as a rate. A window of one to two years has no trough in it.
- **Rankings.** Against the two-year total return, the entry price ranks at Spearman -0.82, the EPP gap at -0.80 and the proxy composite
  at -0.53 (the higher the signals, the worse the outcome).

### 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 42 | +94.4% | +3.3% to +267.3% | 36 | 36 | +85.0% | 36 |
| class RICH | 11 | +51.4% | +26.0% to +81.7% | 10 | 11 | +45.2% | 0 |
| legacy tier BUY | 47 | +91.3% | +3.3% to +267.3% | 41 | 41 | +82.4% | 36 |
| legacy tier ACCUMULATE | 1 | +51.4% | +51.4% to +51.4% | 1 | 1 | +45.2% | 0 |
| legacy tier WATCHLIST | 4 | +45.4% | +40.9% to +48.6% | 4 | 4 | +38.3% | 0 |
| legacy tier AVOID | 1 | +26.0% | +26.0% to +26.0% | 0 | 1 | +27.4% | 0 |
| latest print Q3 2019 (2020-01-03 to 2020-01-17; 3 CHEAP) | 3 | +10.7% | +3.3% to +22.4% | 0 | 0 | -6.3% | 0 |
| latest print Q4 2019 (2020-01-23 to 2020-04-17; 13 CHEAP) | 13 | +115.5% | +24.9% to +267.3% | 10 | 10 | +49.7% | 10 |
| latest print Q1 2020 (2020-04-23 to 2020-07-17; 13 CHEAP) | 13 | +123.7% | +84.2% to +158.4% | 13 | 13 | +80.1% | 13 |
| latest print Q2 2020 (2020-07-23 to 2020-10-16; 10 CHEAP, 3 RICH) | 13 | +76.5% | +52.8% to +91.3% | 13 | 13 | +92.2% | 10 |
| latest print Q3 2020 (2020-10-22 to 2020-12-31; 8 RICH, 3 CHEAP) | 11 | +51.4% | +26.0% to +96.3% | 10 | 11 | +45.2% | 3 |

- **CHEAP held on 36 of 42; RICH held on 0 of 11.** The six CHEAP misses are 2020-01-03 to 2020-02-07, before the collapse (+3% to +31%,
  9-48pp behind SPY). From 2020-02-14 every CHEAP date cleared the hurdle and beat SPY (the March dates by up to +177pp).
- **Every RICH date beat SPY** (by 15-67pp) and 10 of 11 cleared the hurdle. RICH came from a negative BASE (Q2 and Q3 2020 revenue,
  -21% and -14%) applied to the unchanged $0.45: the same reading of a trough quarter as a two-year rate that failed for Baker Hughes
  Incorporated in 2009.
- **Rankings:** entry price -0.81, EPP gap -0.71, proxy composite +0.15.

### 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 29 | +52.9% | +32.7% to +85.6% | 29 | 29 | +33.2% | 29 |
| class RICH | 23 | +37.0% | +16.0% to +52.3% | 13 | 23 | +23.2% | 0 |
| legacy tier BUY | 41 | +49.5% | +25.5% to +85.6% | 39 | 41 | +31.0% | 29 |
| legacy tier ACCUMULATE | 3 | +30.1% | +25.3% to +38.6% | 1 | 3 | +21.6% | 0 |
| legacy tier WATCHLIST | 2 | +20.5% | +20.3% to +20.5% | 0 | 2 | +16.2% | 0 |
| legacy tier AVOID | 6 | +21.5% | +16.0% to +44.6% | 2 | 6 | +13.7% | 0 |
| latest print Q3 2020 (2021-01-08 to 2021-01-15; 2 RICH) | 2 | +44.6% | +39.8% to +44.6% | 2 | 2 | +30.1% | 0 |
| latest print Q4 2020 (2021-01-22 to 2021-04-16; 11 RICH, 2 CHEAP) | 13 | +39.5% | +25.3% to +63.0% | 9 | 13 | +31.0% | 2 |
| latest print Q1 2021 (2021-04-22 to 2021-07-16; 10 RICH, 3 CHEAP) | 13 | +32.7% | +16.0% to +73.9% | 7 | 13 | +18.7% | 3 |
| latest print Q2 2021 (2021-07-22 to 2021-10-15; 13 CHEAP) | 13 | +61.1% | +35.1% to +85.6% | 13 | 13 | +27.4% | 13 |
| latest print Q3 2021 (2021-10-21 to 2021-12-31; 11 CHEAP) | 11 | +48.0% | +32.7% to +56.2% | 11 | 11 | +32.8% | 11 |

- **CHEAP held on all 29; RICH on none of 23.** Every 2021 date beat SPY over two years (by 12-79pp) and 42 of 52 cleared the hurdle;
  the RICH dates returned +16% to +52%. The six AVOID dates were the weakest entries of the year (median +21.5%) and still beat SPY.
- **Rankings:** entry price -0.66, EPP gap -0.60, proxy composite +0.18.

### Across 2019-2021 (hypotheses, not rules)

- **The calls held on 65 of 153 dates: CHEAP 65 of 119, RICH 0 of 34.** By year 0 of 48, 36 of 53 and 29 of 52. Calling every date CHEAP
  would have held on 99, every date RICH on 54: the classification did worse than a constant.
- **RICH failed on every date, the reverse of 2014-2017** (153 of 160). In both periods RICH came from BASE, the latest quarter's
  revenue growth as a two-year rate. It was right while a downturn persisted (2015-2016) and wrong at each turn (2009, 2020-2021).
  This repeats the hypothesis of the earlier sections: test a dampened or mean-reverting BASE for cyclicals, across tickers.
- **A short window cannot tell cheap from dear.** 2019's CHEAP rested on a 1.1- to 2-year window of one stock's P/E on one year's EPS.
  The listing rule produces a class from the first date it can; hypothesis: a minimum window before a class is given (an owner
  question, and a rule change if adopted). AVGO's 2009 dates are the other case to test it on.
- **One year's EPS anchored three years.** $0.45 stood from 2019 to 2021 because 2019 was distorted and 2020 a loss; the quarters'
  adjusted figures summed to $0.83 for 2019, which the method does not read.
- **The entry price ranked the two-year return best** in every year (-0.66 to -0.82; -0.80 over all 153), as in every earlier section.
  The proxy composite ranked it -0.53, +0.15 and +0.18 by year.

## 2022-2026: Baker Hughes Company (253 dates, 2022-01-07 to 2026-11-06)

Scored only after the point-in-time build was committed and pushed (9fcc596) and the firewall had passed at its 28 cutoffs. Outcomes
were computed on 2026-11-10 from the closes posted to 2026-11-09, so the horizons are incomplete: 149 dates have a two-year outcome (to
2024-11-08), 96 a three-year one (to 2023-11-03), 201 a one-year one (to 2025-11-07) and 227 a six-month one. **Nothing below judges a
2025 or 2026 call:** those dates have no two-year outcome yet. Dividends are $0.18 to $0.23 a quarter; no split or special dividend.

**Hindsight the model could not see:** the 2022 sell-off (low close $20.45, in the two-year window of the early-2022 dates), then a rise to $69
in 2026; two-year endpoints of 2023 dates fall in 2025, of 2024 dates in 2026.

### 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 23 | +45.5% | +14.0% to +80.1% | 18 | 17 | +28.7% | 21 |
| class FAIR | 5 | +53.0% | +36.7% to +58.5% | 5 | 2 | +19.3% | 3 |
| class RICH | 24 | +3.7% | -12.8% to +53.5% | 3 | 2 | -0.9% | 20 |
| legacy tier BUY | 32 | +45.5% | +12.1% to +80.1% | 25 | 20 | +25.0% | 26 |
| legacy tier ACCUMULATE | 6 | +12.1% | +4.3% to +47.4% | 1 | 1 | +10.5% | 4 |
| legacy tier WATCHLIST | 1 | +5.0% | +5.0% to +5.0% | 0 | 0 | +2.0% | 1 |
| legacy tier AVOID | 13 | -4.6% | -12.8% to +3.7% | 0 | 0 | -11.0% | 13 |
| latest print Q3 2021 (2022-01-07 to 2022-01-14; 1 CHEAP, 1 RICH) | 2 | +33.7% | +20.3% to +33.7% | 1 | 2 | +23.8% | 1 |
| latest print Q4 2021 (2022-01-21 to 2022-04-14; 10 RICH, 3 CHEAP) | 13 | -3.9% | -12.8% to +18.2% | 0 | 3 | -3.4% | 13 |
| latest print Q1 2022 (2022-04-21 to 2022-07-15; 10 RICH, 3 CHEAP) | 13 | +5.0% | -10.8% to +39.7% | 1 | 0 | +2.0% | 11 |
| latest print Q2 2022 (2022-07-21 to 2022-10-14; 13 CHEAP) | 13 | +50.0% | +39.8% to +80.1% | 13 | 12 | +33.9% | 13 |
| latest print Q3 2022 (2022-10-20 to 2022-12-30; 5 FAIR, 3 CHEAP, 3 RICH) | 11 | +47.4% | +36.7% to +58.8% | 11 | 4 | +19.3% | 6 |

- **The calls held on 44 of 52: the best year of the whole BKR series for the classes.** RICH (the first-half highs, $29-39) held on
  20 of 24 and returned a median +3.7% over two years; CHEAP (the summer lows) held on 21 of 23 at a median +45.5%. All 13 AVOID dates
  missed the hurdle and SPY. Over six months CHEAP beat SPY on 22 of 23 dates and RICH on 2 of 24.
- **Why it worked:** with the EPS fixed at $0.45, the class was a reading of the price against its own four-year range, and 2022 was a
  year when that range held. The misses are at the year's end, where FAIR and RICH dates went on to +37% to +54% but trailed SPY.
- **Rankings.** Against the two-year total return: the entry price at Spearman -0.81, the EPP gap -0.69, the proxy composite -0.84.

### 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 45 | +37.8% | +19.5% to +71.2% | 32 | 10 | +26.8% | 33 |
| class FAIR | 1 | +57.1% | +57.1% to +57.1% | 1 | 1 | +19.9% | 1 |
| class RICH | 6 | +48.4% | +40.2% to +55.7% | 6 | 2 | +14.8% | 0 |
| legacy tier BUY | 45 | +37.8% | +19.5% to +71.2% | 32 | 10 | +26.8% | 32 |
| legacy tier ACCUMULATE | 5 | +55.0% | +46.9% to +57.1% | 5 | 3 | +14.8% | 2 |
| legacy tier WATCHLIST | 2 | +48.4% | +40.2% to +48.4% | 2 | 0 | +15.5% | 0 |
| latest print Q3 2022 (2023-01-06 to 2023-01-20; 3 RICH) | 3 | +48.4% | +46.9% to +55.0% | 3 | 1 | +13.9% | 0 |
| latest print Q4 2022 (2023-01-24 to 2023-04-14; 8 CHEAP, 3 RICH, 1 FAIR) | 12 | +55.0% | +30.0% to +71.2% | 11 | 8 | +29.0% | 9 |
| latest print Q1 2023 (2023-04-20 to 2023-07-14; 13 CHEAP) | 13 | +33.1% | +21.0% to +42.8% | 8 | 1 | +31.7% | 8 |
| latest print Q2 2023 (2023-07-20 to 2023-10-20; 14 CHEAP) | 14 | +32.8% | +19.5% to +50.6% | 7 | 0 | +14.4% | 7 |
| latest print Q3 2023 (2023-10-27 to 2023-12-29; 10 CHEAP) | 10 | +47.2% | +37.9% to +53.7% | 10 | 3 | +27.2% | 10 |

- **Held on 34 of 52.** Every date made money over two years (+19.5% to +71.2%) and 39 cleared the hurdle, but only 13 beat SPY (median
  excess -6.8pp): CHEAP held where it cleared the hurdle, and missed on 12 dates of June to September 2023 (+19.5% to +31.9%, 6-24pp
  behind SPY). The six RICH dates of January to March all cleared the hurdle and so failed. Over one year only 1 of 52 dates beat SPY.
- **Rankings:** entry price -0.36, EPP gap -0.29, proxy composite -0.57.

### 2024 (52 dates; 45 with a two-year outcome)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 45 | +82.6% | +15.0% to +123.8% | 44 | 44 | +52.3% | 44 |
| latest print Q3 2023, EPS $0.45 (2024-01-05 to 2024-01-19) | 3 | +57.7% | +52.1% to +74.3% | 3 | 3 | +38.5% | 3 |
| latest print Q4 2023, EPS $1.60 (2024-01-25 to 2024-04-19) | 13 | +95.5% | +73.4% to +123.8% | 13 | 13 | +46.7% | 13 |
| latest print Q1 2024, EPS $1.60 (2024-04-25 to 2024-07-19) | 13 | +97.0% | +59.5% to +121.5% | 13 | 13 | +53.5% | 13 |
| latest print Q2 2024, EPS $1.60 (2024-07-26 to 2024-10-18) | 13 | +74.3% | +52.4% to +92.5% | 13 | 13 | +57.5% | 13 |
| latest print Q3 2024, EPS $1.60 (2024-10-24 to 2024-11-08) | 3 | +50.7% | +15.0% to +56.8% | 2 | 2 | +52.6% | 2 |

- **CHEAP on every date and it held on 44 of 45** (median +82.6%, +43.3pp over SPY); the one miss is 2024-11-08 (+15.0%). The seven
  dates from 2024-11-15 have no two-year outcome yet. Every two-year endpoint landed nearest the BASE price ($47-69), far under BULL
  ($127-163).
- **Rankings:** entry price -0.76, EPP gap -0.88, proxy composite -0.57.

### 2025 and 2026 (97 dates): no two-year outcome yet

Not judged. For the record only: the 45 dates of 2025 with a one-year outcome (all CHEAP) returned a median +41.1% and 40 beat SPY; of
the 19 dates of 2026 with a six-month outcome, the 13 FAIR dates returned a median -6.1% and none beat SPY, the 5 CHEAP a median +10.1%.

### Across 2022-2024 (hypotheses, not rules)

- **The calls held on 122 of 149 dates with an outcome:** CHEAP 98 of 113, FAIR 4 of 6, RICH 20 of 30. Calling every date CHEAP would
  have held on 114, so the classes added 8 dates, all of them in 2022.
- **The same machinery that failed in 2019-2021 (65 of 153) held here.** Nothing in the method changed between the two periods; the
  stock went sideways and then up. Both results say more about the path of one stock than about the rules. Hypothesis unchanged: a
  class from one stock's short window of its own P/E is mostly "buy lower", and needs many tickers on the same dates to test.
- **RICH held when the price was high in its own range (2022: 20 of 24) and failed when the business was turning up (2020-2021 and
  early 2023: 0 of 40).** It has not once held on a date where BASE was negative from a trough quarter.
- **The switch to the company's adjusted EPS in January 2024 changed no outcome that can be scored yet:** every 2024 date is CHEAP under
  it and under GAAP alike; the two readings part only from 2024-11-08, where there is one scored date.
- **The proxy composite ranked the two-year return negatively in every year** (-0.84, -0.57, -0.57), as in 2019: higher signals went
  with lower returns. A hypothesis for the live model's weighting of trailing growth in a cyclical, to test elsewhere.

## The encoding calls, seen afterwards

**2008-2009.** No judgement call recorded in retro/README.md ("BKR") moves a class or a tier, so every outcome above is the same under
each variant. The variants are:
- 2000 or 1999 excluded (the history and the window from 2001 or 2000);
- GAAP EPS instead of the company's operating profit per share;
- the outside-North-America outlook as BASE where it is a number;
- every signal at its BEAR or XBULL value.

What decided the 2008 failures and the 2009 successes was not an encoding choice. It was two rules of method r2 applied to a cyclical
without guidance: the last full year as the EPS anchor, and a P/E floor from the median of the window's calendar-year lows. Both are
hypotheses to test across tickers (XOM, RCL and MAR showed related early-2008 failures), never a reason to re-encode BKR.

**2010-2013.** Each variant in retro/README.md ("BKR 2010-2013") was rebuilt on every date with one encoding changed, then scored against
the same outcomes. This is hindsight: the class moves were recorded before scoring, in 57e05a9.

| Variant | Classes moved | Call held 2010 | 2011 | 2012 | 2013 | All |
|---|---|---|---|---|---|---|
| as committed (BJ Services in growth as published) | - | 26/52 | 1/52 | 37/52 | 43/53 | 107/209 |
| pro forma comparisons, Q2 2010 to Q1 2011 | 51 (2010-08-04 to 2011-07-22: 31 CHEAP to RICH, 12 CHEAP to FAIR, 8 FAIR to RICH) | 46/52 | 27/52 | 37/52 | 43/53 | 153/209 |
| GAAP EPS in every year | 28 (2011-11-02 to 2013-11-29) | 26/52 | 1/52 | 37/52 | 34/53 | 98/209 |
| PPS-inclusive basis (2011 $4.20, 2012 $2.97) | 3 (2013) | 26/52 | 1/52 | 37/52 | 44/53 | 108/209 |
| 2000 excluded (history and window from 2001) | 3 (2010) | 27/52 | 1/52 | 37/52 | 43/53 | 108/209 |
| industrial segment in revenue outside North America | 0 | 26/52 | 1/52 | 37/52 | 43/53 | 107/209 |
| every signal at its BEAR value | 119 | 44/52 | 29/52 | 40/52 | 30/53 | 143/209 |
| every signal at its XBULL value | 46 | 19/52 | 1/52 | 37/52 | 22/53 | 79/209 |

The as-published growth is the call that decided 2010-2011. It stays as encoded, for three reasons:
- it is method r2's rule, set on PEP, XOM and AVGO;
- it was recorded with its 51-class sensitivity before any 2010-2013 outcome was computed;
- a better score on BKR is not a reason to re-encode BKR.

Testing pro forma growth means a new method version, a reason that does not come from these outcomes, and a full re-run of every
ticker. Every signal at its BEAR value scores well in 2010-2011 because it turns most of those dates FAIR or RICH while the stock went
sideways and then down, and it fails in 2013. It is a stress test, not a candidate encoding.

**2014-2017.** Each variant in retro/README.md ("BKR 2014-2017") was rebuilt on every date with one encoding changed, then scored against
the same outcomes. This is hindsight: the class moves were recorded before scoring, in e026e58.

| Variant | Classes moved | Call held 2014 | 2015 | 2016 | 2017 | All |
|---|---|---|---|---|---|---|
| as committed | - | 43/52 | 40/53 | 51/52 | 21/26 | 155/183 |
| GAAP EPS in every year (2015 and 2016 losses either way) | 12 (2015-01-21 to 2017-06-30: 3 CHEAP to FAIR, 9 FAIR to RICH) | 43/52 | 44/53 | 51/52 | 26/26 | 164/183 |
| 2012 at $3.00, no restatement | 0 | 43/52 | 40/53 | 51/52 | 21/26 | 155/183 |
| industrial segment in revenue outside North America | 0 | 43/52 | 40/53 | 51/52 | 21/26 | 155/183 |
| every signal at its BEAR value | 23 | 46/52 | 51/53 | 51/52 | 26/26 | 174/183 |
| every signal at its XBULL value | 75 (2015-05-29 to 2016-10-26: 53 RICH to CHEAP) | 43/52 | 8/53 | 10/52 | 21/26 | 82/183 |

No call is re-encoded on these scores. GAAP EPS scores better here (FY14 at $3.92 lowers the stale anchor), but it scored worse in 2013;
the company's figures are the house rule (ACN). Every signal at BEAR scores well because it reads RICH almost everywhere while the stock
fell; it is a stress test, not a candidate encoding. Every signal at XBULL shows how much the RICH calls of 2015-2016 rest on the
signals reading the revenue fall.

**2019-2021.** Each variant in retro/README.md ("BKR 2018-2021") was rebuilt on every date with one encoding changed, then scored against
the same outcomes. This is hindsight: the class moves were recorded before scoring, in e9e8e19.

| Variant | Classes moved | Call held 2019 | 2020 | 2021 | All |
|---|---|---|---|---|---|
| as committed | - | 0/48 | 36/53 | 29/52 | 65/153 |
| 2019 kept at GAAP $0.23 | 61 | 0/48 | 10/53 | 0/52 | 10/153 |
| adjusted quarters summed (2018 $0.64, 2019 $0.83), 2020 excluded | 34 | 0/48 | 47/53 | 52/52 | 99/153 |
| adjusted quarters summed, 2020 kept at $0.03 | 42 | 0/48 | 47/53 | 2/52 | 49/153 |
| 2018 at $0.64, 2019 and 2020 excluded | 1 | 0/48 | 36/53 | 28/52 | 64/153 |
| Class A share count alone | 40 | 0/48 | 20/53 | 5/52 | 25/153 |
| no buyback term | 10 | 0/48 | 31/53 | 24/52 | 55/153 |
| rule T: 2018 orders and segment margin as GAAP | 0 | 0/48 | 36/53 | 29/52 | 65/153 |
| every signal at its BEAR value | 41 | 6/48 | 32/53 | 8/52 | 46/153 |
| every signal at its XBULL value | 27 | 0/48 | 41/53 | 41/52 | 82/153 |

No variant rescues 2019. The spread from 10 to 99 of 153 comes from which years are in the EPS history and which share count feeds the
buyback term: the outcome of this series depends more on those two encoding calls than on anything the company reported. That is a
reason to treat these 153 labels as weak evidence, not a reason to pick the variant that scored best.

**2022-2026.** Each variant in retro/README.md ("BKR 2022-2026") was rebuilt on every date with one encoding changed, then scored against
the same outcomes (the 149 dates that have one). This is hindsight: the class moves were recorded before scoring, in 9fcc596.

| Variant | Classes moved (dates with an outcome) | Call held 2022 | 2023 | 2024 | All |
|---|---|---|---|---|---|
| as committed | - | 44/52 | 34/52 | 44/45 | 122/149 |
| GAAP EPS in 2023-2025 | 1 | 44/52 | 34/52 | 45/45 | 123/149 |
| 2022 not taken from the Q4 2023 release | 1 | 44/52 | 34/52 | 45/45 | 123/149 |
| adjusted quarters summed for 2018-2022 | 29 | 28/52 | 37/52 | 44/45 | 109/149 |
| Class A share count alone | 72 | 26/52 | 12/52 | 42/45 | 80/149 |
| no buyback term | 18 | 37/52 | 31/52 | 44/45 | 112/149 |
| FY2026 revenue guide not used | 0 | 44/52 | 34/52 | 44/45 | 122/149 |
| every signal at its BEAR value | 62 | 26/52 | 19/52 | 45/45 | 90/149 |
| every signal at its XBULL value | 23 | 47/52 | 40/52 | 44/45 | 131/149 |

The EPS calls of 2024 (adjusted against GAAP, 2022 in or out) cannot be told apart yet: they move 50 and 41 classes, all but one on
dates without an outcome. The share count is again the encoding the result depends on most. The summed-quarters variant, which scored
best for 2019-2021, scores worse here: no variant is better in both periods.
