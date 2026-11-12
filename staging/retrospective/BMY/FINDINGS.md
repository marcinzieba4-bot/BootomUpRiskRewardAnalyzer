# BMY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the BMY weekly dates: 732 from 2008-01-04 to 2021-12-31, all Bristol-Myers Squibb Company (NYSE: BMY).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 4821356, firewall result 36e19d3; 2010-2013: 31cea6e, controls and firewall
result 533d892; 2014-2017: 20cbe3e, controls and leak scan 932ebbb, firewall result 3921459; 2018-2021: 2304926, controls, leak scan and
firewall result 5c1e9d5); the outcomes were computed on 2026-11-12. Every date has its 6-month, 1-, 2- and 3-year horizons (the last
ends 2024-12-30). Total returns include the quarterly dividends ($0.31
from the ex-date of 2008-01-02, $0.32 from 2009-12-30, $0.33 from 2011-01-05, $0.34 from 2012-01-04, $0.35 from 2013-01-02, $0.36 from
2013-12-31, $0.37 from 2014-12-30, $0.38 from 2015-12-30, $0.39 from 2017-01-04, $0.40 from 2018-01-04, $0.41 from 2019-01-03, $0.45 from
2020-01-02, $0.49 from 2020-12-31, $0.54 from 2022-01-06, $0.57 from 2023-01-05, $0.60 from 2024-01-04). Each December's new rate was stated in no filing before the next 10-K, so the models from the declaration to the 10-K carry
the old rate ($0.31 from 2009-12-24 to 2010-02-12, $0.32 to 2011-02-11, and likewise later: $0.35 to 2014-02-07, $0.36 to 2015-02-06,
$0.37 to 2016-02-05, $0.38 to 2017-02-17, $0.39 to 2018-02-06, $0.40 to 2019-02-22, $0.41 to 2020-02-21, $0.45 to 2021-02-05, and $0.49
through December 2021; checked after scoring; no model changes). No
split falls in any horizon, so every price is as traded (the Celgene acquisition issued new BMY shares to Celgene's holders and needs no
factor); the Mead Johnson split-off of 2009-12-23 was an exchange offer, so a holder who
did not tender kept the same shares and Yahoo's series needs no factor. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should
clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the benchmark, and RICH should miss the hurdle and lag the
benchmark.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 49 | +31.2% | +12.1% to +69.4% | 24 | 42 | +11.0% | 45 |
| class CHEAP, legacy tier ACCUMULATE | 2 | +16.8% | +12.6% to +16.8% | 0 | 2 | -4.7% | 2 |
| class CHEAP, legacy tier WATCHLIST | 1 | +9.2% | +9.2% | 0 | 1 | -15.6% | 1 |
| class FAIR, legacy tier WATCHLIST | 1 | +4.1% | +4.1% | 0 | 1 | -17.8% | 0 |
| FY07E $1.175 (2008-01-04 to 2008-01-25) | 4 | +12.6% | +4.1% to +16.8% | 0 | 4 | -10.9% | 3 |
| FY08E $1.41 (2008-02-01 to 2008-10-17) | 38 | +30.9% | +12.1% to +69.4% | 17 | 38 | +8.9% | 38 |
| FY08E $1.635 (2008-10-24 to 2008-12-31) | 11 | +35.6% | +23.3% to +67.1% | 7 | 4 | +23.5% | 7 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | +12.6% | +4.1% to +16.8% | 0 | 4 | -10.9% | 3 |
| latest print Q4 2007 (2008-02-01 to 2008-04-18) | 12 | +26.9% | +12.1% to +37.5% | 5 | 12 | +2.2% | 12 |
| latest print Q1 2008 (2008-04-25 to 2008-07-18) | 13 | +23.6% | +12.8% to +44.5% | 4 | 13 | +8.3% | 13 |
| latest print Q2 2008 (2008-07-25 to 2008-10-17) | 13 | +34.2% | +22.7% to +69.4% | 8 | 13 | +14.7% | 13 |
| latest print Q3 2008 (2008-10-24 to 2008-12-31) | 11 | +35.6% | +23.3% to +67.1% | 7 | 4 | +23.5% | 7 |

- **CHEAP held on 48 of 52 dates, nearly all by beating SPY.** The 45 CHEAP dates to 2008-11-14 ($17.54-25.75) returned +9.2% to +69.4%
  over two years, dividends included, while SPY returned -18.7% to +44.0%; every one beat it, by 1.8-56.1pp, and 21 cleared the hurdle.
  The next three (2008-11-21 to 2008-12-05) lagged SPY's rebound but cleared the hurdle (+33.9% to +49.0%). The four misses are the last
  four dates of the year (2008-12-12 to 2008-12-31, $22.51-23.25): +23.3% to +27.2%, under the hurdle and
  18-24pp behind SPY's rebound from its March 2009 low. The one FAIR date (2008-01-11, $26.48) returned +4.1% and beat SPY by 18.8pp, outside
  the ±15pp band, so its call missed; the CHEAP and WATCHLIST date before it (2008-01-04) held. Every 2008 date sat through a 27-36%
  drawdown (low closes $17.26 on 2008-10-16 and $17.51 on 2009-03-03). Over three years (to the end of 2011) the 2008 dates returned
  +11.0% to +108.8% (median +49.6%); all 53 beat SPY and 25 cleared the three-year hurdle.
- **The floor sat above the price and worked as a target.** From the Q4 2007 print the EPP floor (18-19x the GAAP guide, $25-31) sat
  6-43% over the price, set by the window's calendar-year lows for 2006 and 2007 (26-33x, multiples of earnings cut by the generic
  clopidogrel launch, the restatements for discontinued businesses and the restructuring charges). The price reached it within two years
  on 37 of the 53 dates (the two-year highs were $26-28 in 2009-2010); it did not on the five dates of late February and March 2008 ($27
  floor) or the eleven from the Q3 2008 print ($31 floor, on the $1.635 guide that included the ImClone gain). The earnings the guides
  carried were real: FY2008 came in at $1.59 against the $1.41-1.635 the models used, and FY2009 at $1.63 from continuing operations
  without Mead Johnson against $1.51-1.56 (the Q4 2009 release, outside the series). Hypothesis, not a rule: a floor from lows that are
  multiples of depressed earnings marks a recovery level, not a support; test it on other tickers and periods, never fit it to BMY.
- **The ranks run through the price.** Across the 53 dates the entry price ranks the two-year return at Spearman -0.87 and the return to
  the m12-24 average price at -0.84, and the EPP gap at -0.81 and -0.90 (the right signs); Ratio B at -0.49 and -0.27; the adjusted gap at
  +0.21 and -0.14 and the proxy composite at -0.33 and -0.66 (no information, or the wrong sign: the composite was 3.50 on the entries of
  January-April 2008, which returned the least).
- **The two-year price landed nearest BASE on 37 dates and BEAR on 16** (twelve from the Q4 2007 print to 2008-04-18, when BASE was
  that quarter's +27.6%/yr and the BASE price $50-52, and four of May-June 2008), at 0.47-0.73 times the BASE price and 3.7-5.1 times
  BEAR.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +47.3% | +22.4% to +63.7% | 45 | 34 | +23.9% | 46 |
| FY08E $1.635 (2009-01-09 to 2009-01-23) | 3 | +27.7% | +26.8% to +28.6% | 0 | 0 | +14.8% | 0 |
| FY09E $1.655 (2009-01-28 to 2009-07-17) | 25 | +51.1% | +22.4% to +63.7% | 22 | 10 | +29.0% | 22 |
| FY09E $1.63 (2009-07-24 to 2009-10-16) | 13 | +43.7% | +35.0% to +55.7% | 13 | 13 | +22.6% | 13 |
| FY09E $1.745 (2009-10-23 to 2009-12-18) | 9 | +42.8% | +29.1% to +59.1% | 8 | 9 | +15.0% | 9 |
| FY09E $1.535 (2009-12-24 to 2009-12-31) | 2 | +48.6% | +46.4% to +48.6% | 2 | 2 | +14.5% | 2 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +27.7% | +26.8% to +28.6% | 0 | 0 | +14.8% | 0 |
| latest print Q4 2008 (2009-01-28 to 2009-04-24) | 13 | +43.9% | +22.4% to +57.9% | 10 | 0 | +26.1% | 10 |
| latest print Q1 2009 (2009-04-29 to 2009-07-17) | 12 | +55.8% | +46.2% to +63.7% | 12 | 10 | +32.7% | 12 |
| latest print Q2 2009 (2009-07-24 to 2009-10-16) | 13 | +43.7% | +35.0% to +55.7% | 13 | 13 | +22.6% | 13 |
| latest print Q3 2009 (2009-10-23 to 2009-12-31) | 11 | +46.4% | +29.1% to +59.1% | 10 | 11 | +14.5% | 11 |

- **CHEAP held on 46 of 52 dates, mostly by clearing the hurdle.** The 2009 dates returned +22.4% to +63.7% over two years (median
  +47.3%); 45 cleared the hurdle. The six misses are 2009-01-09 to 2009-02-13 ($21.75-23.07): +22.4% to +28.6%, under the hurdle and
  21-39pp behind SPY, whose two years from those dates ran from near its low. From 2009-02-20 every date cleared the hurdle except
  2009-11-27 (+29.1%, which beat SPY), and from 2009-07-24 every date also beat SPY (by 8-43pp). Drawdowns within two years were
  17-24%.
- **The three-year read is cleaner.** Over three years (to the end of 2012) the 2009 dates returned +40.8% to +100.5% (median +70.7%);
  45 beat SPY and 45 cleared the three-year hurdle.
- **The guide and the price moved; the class did not.** The FY09 GAAP guide went from $1.58-1.73 to $1.58-1.68, $1.72-1.77 and, without
  Mead Johnson, $1.51-1.56; BASE fell from +7.5% to +6.5%/yr and the proxy composite from 2.80 to 2.45 and back to 2.80; the price state
  stayed CHEAP at 11.1-16.8x. Within the year the entry price ranks the return to the m12-24 average price at Spearman -0.95 and the
  two-year return at -0.54; the EPP gap at -0.95 and -0.59 and Ratio B at -0.90 and -0.53 (the right signs); the proxy composite at
  -0.55 and -0.56 and the adjusted gap at -0.08 and -0.38 (the wrong sign or none).
- **The two-year price landed nearest BASE on all 52 dates,** at 0.58-1.04 times the BASE price, 0.41-0.63 times BULL and 4.2-8.8 times
  the BEAR price: BEAR (the 2006 fall carried at -49% to -54%/yr) was never close, which is the window's 2006 restated EPS, not the
  business.

## Across 2008-2009

- **The call held on 94 of 105 dates.** The misses are the FAIR date of 2008-01-11 (beat SPY by more than the band), the four CHEAP dates
  of late December 2008 and the six of January-February 2009: all positive (+22.4% to +28.6% for the CHEAP misses) but under the hurdle
  and behind SPY's rebound. PFE's CHEAP dates of October 2008 to January 2009 lagged the same rebound
  (staging/retrospective/PFE/FINDINGS.md), each series scored separately; a hypothesis about the benchmark leg of the test around a market
  low, not about either stock.
- **What the method did not read.** Two events of the period move the business but no model input: the Mead Johnson IPO (February 2009)
  and split-off (December 2009), which retired 269 million BMY shares for a business that was 14% of 2008's net sales, and the PLAVIX
  patent ruling the FY2008 10-K reports (the Court of Appeals "affirmed the District Court's ruling sustaining the validity of the '265
  patent" on December 12, 2008), which the models quote only through the risk factors. The class rested on the GAAP guides against the
  stock's own multiples, and both held for these two years.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +38.6% | +30.0% to +61.8% | 48 | 47 | +24.2% | 49 |
| FY09E $1.535 (2010-01-08 to 2010-01-22) | 3 | +45.3% | +43.4% to +48.4% | 3 | 3 | +17.1% | 3 |
| FY10E $1.99 (2010-01-29 to 2010-04-23) | 13 | +40.6% | +33.8% to +47.9% | 13 | 13 | +19.8% | 13 |
| FY10E $1.89 (2010-04-30 to 2010-12-31) | 36 | +36.2% | +30.0% to +61.8% | 32 | 31 | +26.0% | 33 |
| latest print Q3 2009 (2010-01-08 to 2010-01-22) | 3 | +45.3% | +43.4% to +48.4% | 3 | 3 | +17.1% | 3 |
| latest print Q4 2009 (2010-01-29 to 2010-04-23) | 13 | +40.6% | +33.8% to +47.9% | 13 | 13 | +19.8% | 13 |
| latest print Q1 2010 (2010-04-30 to 2010-07-16) | 12 | +50.9% | +42.3% to +61.8% | 12 | 12 | +28.3% | 12 |
| latest print Q2 2010 (2010-07-23 to 2010-10-22) | 14 | +33.7% | +30.0% to +53.7% | 11 | 9 | +23.9% | 11 |
| latest print Q3 2010 (2010-10-27 to 2010-12-31) | 10 | +34.0% | +30.6% to +38.6% | 9 | 10 | +28.2% | 10 |

- **CHEAP held on 49 of 52 dates.** The 2010 dates ($22.44-27.62) returned +30.0% to +61.8% over two years (median +38.6%), dividends
  included; 48 cleared the hurdle and 47 beat SPY (+15.7% to +38.6%). The three misses are 2010-08-13, 2010-08-20 and 2010-09-17
  ($26.32-27.31): +30.0% to +30.8%, just under the hurdle and 3.6-7.1pp behind SPY. Drawdowns within two years were 11-17%. Over three years
  (to the end of 2013) the 2010 dates returned +51.0% to +126.6% (median +86.8%); all 52 beat SPY and 51 cleared the three-year hurdle.
- **The floor was a target again.** The price sat under the floor on 49 dates and reached it within two years on 39; the ten that did not
  are the dates from the FY2009 10-K to the Q1 2010 print, whose floor (18x FY10E $1.99, $35.82) the two-year high ($35.29 on 2011-12-21)
  missed by 1.5%. The guides were close: FY2010 came in at $1.79 against the $1.89-1.99 the models used.
- **The ranks run through the price, not the signals.** Within 2010 the entry price ranks the two-year return at Spearman -0.87 and the
  return to the m12-24 average price at -0.37, the EPP gap at -0.51 and -0.38 and Ratio B at -0.55 and -0.15 (the right signs); the adjusted
  gap at +0.76 and +0.07 and the proxy composite at +0.73 and -0.05.
- **The two-year price landed nearest BASE on all 52 dates,** at 0.65-1.02 times the BASE price and 0.34-0.62 times BULL; BEAR (the 2006
  restated fall at -65%/yr, a BEAR price of $3) was 5-12 times under it.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 5 | +59.8% | +56.8% to +65.5% | 5 | 5 | +25.7% | 5 |
| class CHEAP, legacy tier BUY | 47 | +57.9% | +39.9% to +84.4% | 47 | 47 | +28.0% | 47 |
| FY10E $1.89 (2011-01-07 to 2011-01-21) | 3 | +42.6% | +39.9% to +42.9% | 3 | 3 | +28.8% | 3 |
| FY11E $2.05 (2011-01-28 to 2011-07-22) | 26 | +57.9% | +49.2% to +82.3% | 26 | 26 | +27.8% | 26 |
| FY11E $2.13 (2011-07-29 to 2011-10-21) | 13 | +57.2% | +53.2% to +69.0% | 13 | 13 | +30.7% | 13 |
| FY11E $2.155 (2011-10-28 to 2011-12-30) | 10 | +70.7% | +56.8% to +84.4% | 10 | 10 | +29.1% | 10 |
| latest print Q3 2010 (2011-01-07 to 2011-01-21) | 3 | +42.6% | +39.9% to +42.9% | 3 | 3 | +28.8% | 3 |
| latest print Q4 2010 (2011-01-28 to 2011-04-21) | 13 | +55.9% | +50.0% to +64.4% | 13 | 13 | +29.3% | 13 |
| latest print Q1 2011 (2011-04-29 to 2011-07-22) | 13 | +63.8% | +49.2% to +82.3% | 13 | 13 | +26.3% | 13 |
| latest print Q2 2011 (2011-07-29 to 2011-10-21) | 13 | +57.2% | +53.2% to +69.0% | 13 | 13 | +30.7% | 13 |
| latest print Q3 2011 (2011-10-28 to 2011-12-30) | 10 | +70.7% | +56.8% to +84.4% | 10 | 10 | +29.1% | 10 |

- **CHEAP held on all 52 dates,** by both legs: +39.9% to +84.4% over two years (median +57.9%) against SPY's +16.9% to +60.6%, ahead by
  2.2-49.3pp. Every date's worst drawdown within two years was the same 14.8%. Over three years (to the end of 2014) +63.7% to +131.4%
  (median +91.3%); all 52 cleared the three-year hurdle and 49 beat SPY.
- **The price reached the floor within two years on all 50 dates that sat under it** (16x, $30.24-34.48). FY2011 came in at $2.16 against
  the $2.05-2.155 the models used.
- **No rank information within the year:** the entry price ranks the two-year return at +0.32 and the m12-24 return at -0.37, the EPP gap at
  +0.19 and -0.54, Ratio B at +0.30 and -0.57, the adjusted gap at +0.32 and +0.43 and the proxy composite at +0.39 and +0.12. The five
  ACCUMULATE dates of December 2011, the year's highest prices, returned +56.8% to +65.5%.
- **The two-year price landed nearest BASE on all 52 dates,** at 0.77-1.11 times the BASE price and 0.51-0.74 times BULL.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 6 | +72.1% | +59.4% to +75.0% | 6 | 6 | +39.9% | 6 |
| class CHEAP, legacy tier WATCHLIST | 6 | +73.5% | +58.7% to +78.1% | 6 | 6 | +43.0% | 6 |
| class FAIR, legacy tier WATCHLIST | 19 | +56.4% | +43.1% to +71.1% | 19 | 12 | +43.1% | 11 |
| class RICH, legacy tier AVOID | 11 | +89.7% | +45.8% to +97.0% | 11 | 10 | +58.5% | 0 |
| class RICH, legacy tier WATCHLIST | 10 | +61.2% | +57.5% to +62.7% | 10 | 10 | +52.3% | 0 |
| FY11E $2.155 (2012-01-06 to 2012-01-20) | 3 | +72.2% | +62.0% to +75.0% | 3 | 3 | +31.6% | 3 |
| FY12E $1.95 (2012-01-27 to 2012-07-20) | 26 | +58.7% | +43.1% to +78.1% | 26 | 19 | +42.7% | 20 |
| FY12E $1.83 (2012-07-26 to 2012-10-19) | 13 | +61.2% | +45.8% to +66.3% | 13 | 12 | +52.3% | 0 |
| FY12E $1.00 (2012-10-25 to 2012-12-28) | 10 | +89.8% | +67.4% to +97.0% | 10 | 10 | +58.8% | 0 |
| latest print Q3 2011 (2012-01-06 to 2012-01-20) | 3 | +72.2% | +62.0% to +75.0% | 3 | 3 | +31.6% | 3 |
| latest print Q4 2011 (2012-01-27 to 2012-04-20) | 13 | +66.4% | +52.7% to +78.1% | 13 | 13 | +42.5% | 10 |
| latest print Q1 2012 (2012-04-27 to 2012-07-20) | 13 | +48.1% | +43.1% to +63.0% | 13 | 6 | +43.7% | 10 |
| latest print Q2 2012 (2012-07-26 to 2012-10-19) | 13 | +61.2% | +45.8% to +66.3% | 13 | 12 | +52.3% | 0 |
| latest print Q3 2012 (2012-10-25 to 2012-12-28) | 10 | +89.8% | +67.4% to +97.0% | 10 | 10 | +58.8% | 0 |

- **CHEAP held on all 12 dates, FAIR on 11 of 19, RICH on none of 21.** Every 2012 date ($31.57-35.95) returned +43.1% to +97.0% over two
  years and cleared the hurdle; SPY returned +34.3% to +55.5%. The eight FAIR misses (the six FAIR dates from 2012-03-16 to 2012-05-11 but
  2012-04-20, and 2012-08-10 and 2012-08-17) beat SPY by 15.5-35.3pp, outside the band; the eleven that held landed -8.9pp to +12.7pp from
  it. The RICH dates returned +45.8% to +97.0% and beat SPY on 20 of 21 (2012-07-26 lagged by 4.4pp, but cleared the hurdle). The ten RICH
  dates from the Q3 2012 print (FY12E $1.00 after the BMS-986094 impairment, 31.7-34.5x) returned the most of the year: +67.4% to +97.0%.
- **Over three years (to the end of 2015)** every 2012 date returned +83.0% to +130.4% (median +107.4%), beat SPY and cleared the hurdle.
- **The weakest prints preceded the best returns.** The entry price ranks the two-year return at -0.71 and the m12-24 return at -0.57 (the
  right sign); the EPP gap at +0.03 and +0.30 and Ratio B at +0.13 and +0.65 carry nothing or the wrong sign; the adjusted gap at -0.20 and
  -0.74 and the proxy composite at -0.30 and -0.82 the wrong sign: the composite fell to 1.65 and 1.45 on the Q2 and Q3 2012 prints (U.S.
  sales -27.3% as PLAVIX lost exclusivity, the impairment), and those dates returned the most.
- **The floor sat under the price on every date.** The price fell to it within two years on the 31 CHEAP and FAIR dates and the 11 RICH
  dates of the Q2 2012 print (floors $31.11-32.32; the close of $30.81 on 2012-11-15), never on the ten from the Q3 2012 print ($18.00).
  FY2012 came in at $1.16 against the $1.00 of the Q3 guide.
- **The two-year price landed nearest BULL on 49 dates and BASE on 3,** at 1.1-4.7 times the BASE price (BASE was -15%/yr on the FY2012
  sales guide) and 0.74-1.57 times BULL.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +55.8% | +27.9% to +89.1% | 50 | 53 | +34.0% | 0 |
| FY12E $1.00 (2013-01-04 to 2013-01-18) | 3 | +87.0% | +85.1% to +89.1% | 3 | 3 | +53.4% | 0 |
| FY13E $1.59 (2013-01-25 to 2013-07-19) | 26 | +65.8% | +45.4% to +81.8% | 26 | 26 | +34.5% | 0 |
| FY13E $1.45 (2013-07-26 to 2013-12-31) | 24 | +37.9% | +27.9% to +58.3% | 21 | 24 | +30.9% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-01-18) | 3 | +87.0% | +85.1% to +89.1% | 3 | 3 | +53.4% | 0 |
| latest print Q4 2012 (2013-01-25 to 2013-04-19) | 13 | +71.7% | +62.8% to +81.8% | 13 | 13 | +43.2% | 0 |
| latest print Q1 2013 (2013-04-26 to 2013-07-19) | 13 | +57.6% | +45.4% to +72.4% | 13 | 13 | +30.2% | 0 |
| latest print Q2 2013 (2013-07-26 to 2013-10-18) | 13 | +43.7% | +35.0% to +58.3% | 13 | 13 | +37.6% | 0 |
| latest print Q3 2013 (2013-10-24 to 2013-12-31) | 11 | +35.3% | +27.9% to +42.1% | 8 | 11 | +21.1% | 0 |

- **RICH held on none of 53 dates.** The stock rose from $33.35 to $53.41 through the year and still returned +27.9% to +89.1% over two
  years (median +55.8%); all 53 beat SPY (by 7.7-48.3pp) and 50 cleared the hurdle. The three under it are 2013-11-01 to 2013-11-15
  ($52.35-52.48, +27.9% to +31.2%), which still beat SPY.
- **Three years tells the other story for the last dates.** The 13 dates from 2013-10-11 ($47.68-53.41, 34-37x FY13E) returned only +5.3% to
  +21.4% over three years (to late 2016), under the hurdle and 9.9-21.4pp behind SPY: the price that the two-year horizon left at $61-70
  fell back to $50-58 by late 2016. Over three years 37 of the 53 dates beat SPY and 33 cleared the hurdle; by `call_check_2y` none held.
- **The ranks were right; the level was not.** Within 2013 the entry price ranks the two-year return at -0.94 and the m12-24 return at
  -0.87, the EPP gap at -0.75 and -0.55, Ratio B at -0.82 and -0.62 and the proxy composite at -0.73 and -0.37: the richer the date, the
  less it returned, but every date returned more than SPY. The floor ($26.10-29.00) was never reached (lowest close within two years $33.40,
  on 2013-01-07).
- **The earnings were not the surprise.** FY2013 came in at $1.54 GAAP against the $1.45-1.59 the models used (the Q4 2013 release of
  2014-01-24, outside the series), and FY2012 at $1.16 against $1.00. The multiple carried the return: the two-year price landed nearest
  BULL on all 53 dates, at 1.30-1.70 times the BULL price ($39-46 on the 2003-2012 CAGR of -3.0%/yr) and 2.1-4.8 times BASE.

## Across 2010-2013

- **The call held on 124 of 209 dates:** CHEAP on 113 of 116 (2010 to 2012-04-13), FAIR on 11 of 19, RICH on none of 74 (2012-07-26 to
  2013-12-31). With 2008-2009, the call held on 218 of 314 dates; CHEAP on 207 of 220.
- **The RICH calls failed on a patent cliff.** They rest on GAAP EPS at a trough (PLAVIX's U.S. exclusivity lost in May 2012 and
  AVAPRO/AVALIDE's in March 2012, the $1.8 billion impairment) against the stock's own P/E history, and on BASE from sales guides 4-19%
  under the year before. The two-year returns came from the multiple, which the market set on what came next; with hindsight, the product
  cycle that followed (YERVOY from 2011, ELIQUIS approved in December 2012, the PD-1 antibody nivolumab, approved as Opdivo in December
  2014) is nowhere in the model's inputs, and no point-in-time rule could have read it as a number. Hypothesis, not a rule: on an
  exclusivity loss, a P/E on trough GAAP earnings ranked against the stock's own past flags RICH while the market prices the successors;
  test it on other series and periods, never fit it to BMY or carry it into a BMY model.
- **Weak signals marked the best entries.** In 2012 the lowest proxy composites (1.45-1.65, the PLAVIX quarters) came before the highest
  returns, as the 2008 composite of 3.50 came before the lowest; across the four years the composite carries no reliable sign. The entry
  price ranks the returns in the right direction in 2010, 2012 and 2013.
- **BEAR was never close.** The two-year price was 5-35 times the BEAR price on every date: BEAR is the FY2009 10-K's restated 2006 fall
  (-65%/yr to $0.40), method behaviour on the window, not the business.


## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +24.4% | -7.2% to +63.5% | 20 | 39 | +29.5% | 13 |
| FY13E $1.45 (2014-01-03 to 2014-01-17) | 3 | +20.9% | +18.5% to +35.7% | 1 | 3 | +19.0% | 0 |
| FY14E $1.825 (2014-01-24 to 2014-04-25) | 14 | +26.8% | +16.1% to +45.7% | 5 | 14 | +27.0% | 0 |
| FY14E $1.75 (2014-04-30 to 2014-07-18) | 12 | +55.4% | +45.2% to +63.5% | 12 | 12 | +34.6% | 0 |
| FY14E $1.55 (2014-07-25 to 2014-10-17) | 13 | +18.0% | +3.8% to +59.0% | 2 | 10 | +31.2% | 3 |
| FY14E $1.2 (2014-10-24 to 2014-12-26) | 10 | +1.4% | -7.2% to +5.1% | 0 | 0 | +9.5% | 10 |
| latest print Q3 2013 (2014-01-03 to 2014-01-17) | 3 | +20.9% | +18.5% to +35.7% | 1 | 3 | +19.0% | 0 |
| latest print Q4 2013 (2014-01-24 to 2014-04-25) | 14 | +26.8% | +16.1% to +45.7% | 5 | 14 | +27.0% | 0 |
| latest print Q1 2014 (2014-04-30 to 2014-07-18) | 12 | +55.4% | +45.2% to +63.5% | 12 | 12 | +34.6% | 0 |
| latest print Q2 2014 (2014-07-25 to 2014-10-17) | 13 | +18.0% | +3.8% to +59.0% | 2 | 10 | +31.2% | 3 |
| latest print Q3 2014 (2014-10-24 to 2014-12-26) | 10 | +1.4% | -7.2% to +5.1% | 0 | 0 | +9.5% | 10 |

- **RICH held on 13 of 52 dates, all from October.** The 39 RICH dates from 2014-01-03 to 2014-09-26 ($47.09-56.18, 27-39x the GAAP
  guides) returned +12.7% to +63.5% over two years, dividends included, beat SPY by 1.8-51.1pp, and 20 cleared the hurdle; the twelve
  from the Q1 2014 print (FY14E $1.75, the year's lowest prices, $47.09-51.18) returned +45.2% to +63.5%. The 13 that held run from
  2014-10-03 to 2014-12-26 ($50.28-61.30, the last three dates on the Q2 2014 guide and all ten on the Q3 2014 guide of $1.20, at
  45-52x): -7.2% to +12.6%, 1.5-16.8pp behind SPY, none over the hurdle.
- **The floor was never reached and the price landed nearest BULL on every date,** at 0.88-1.68 times the BULL price (BULL at +4.7%/yr,
  the 2004-2013 CAGR, from the Q1 2014 print). The lowest close within two years was $46.59-49.34 against floors of $25.20-38.32.
- **Three years is uniform:** +4.9% to +38.6% to late 2017, none over the three-year hurdle and 51 of 52 behind SPY.
- **The ranks run through the price.** The entry price ranks the two-year return at Spearman -0.83 and the return to the m12-24 average
  price at -0.97, the EPP gap at -0.82 and -0.67, Ratio B (40 finite dates) at -0.42 and +0.07; the adjusted gap at +0.76 and +0.50 and
  the proxy composite at +0.56 and +0.12 (the right signs).

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | -7.1% | -17.2% to +11.1% | 0 | 0 | -10.8% | 53 |
| FY14E $1.2 (2015-01-02 to 2015-01-23) | 4 | +2.6% | -14.6% to +4.0% | 0 | 0 | +4.5% | 4 |
| FY15E $1.625 (2015-01-28 to 2015-04-24) | 13 | -9.8% | -17.2% to -2.2% | 0 | 0 | -5.2% | 13 |
| FY15E $1.01 (2015-04-29 to 2015-07-17) | 12 | -13.4% | -16.5% to -8.1% | 0 | 0 | -12.2% | 12 |
| FY15E $1.07 (2015-07-24 to 2015-10-23) | 14 | +2.6% | -11.1% to +11.1% | 0 | 0 | -10.6% | 14 |
| FY15E $1.045 (2015-10-28 to 2015-12-31) | 10 | -4.7% | -7.1% to -0.1% | 0 | 0 | -15.8% | 10 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +2.6% | -14.6% to +4.0% | 0 | 0 | +4.5% | 4 |
| latest print Q4 2014 (2015-01-28 to 2015-04-24) | 13 | -9.8% | -17.2% to -2.2% | 0 | 0 | -5.2% | 13 |
| latest print Q1 2015 (2015-04-29 to 2015-07-17) | 12 | -13.4% | -16.5% to -8.1% | 0 | 0 | -12.2% | 12 |
| latest print Q2 2015 (2015-07-24 to 2015-10-23) | 14 | +2.6% | -11.1% to +11.1% | 0 | 0 | -10.6% | 14 |
| latest print Q3 2015 (2015-10-28 to 2015-12-31) | 10 | -4.7% | -7.1% to -0.1% | 0 | 0 | -15.8% | 10 |

- **RICH held on all 53 dates.** At 37-69x the GAAP guides ($57.30-69.29) the stock returned -17.2% to +11.1% over two years (median
  -7.1%), 10.4-42.5pp behind SPY, none over the hurdle; over three years (to late 2018) -22.5% to +18.9%, all behind SPY. Every date sat
  through a 36-39% drawdown inside its two years, from the high of $76.77 on 2016-07-14.
- **The two-year price landed nearest BULL on 49 dates** (0.77-1.32 times the BULL price, BULL at +0.5% to +4.0%/yr) and BASE on 4;
  the floor ($21.21-34.12) was never reached.
- **The guides overstated the year less than the multiple did.** FY2015 came in at $0.97 GAAP in the Q4 2015 release ($0.93 in the
  10-K) against the $1.01-1.625 the models used; the price fell back from a multiple that, on any of those figures, sat at the top of the
  stock's own range.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 23 | +5.6% | -11.1% to +21.9% | 0 | 0 | +4.7% | 0 |
| class CHEAP, legacy tier ACCUMULATE | 14 | -17.5% | -23.5% to +15.2% | 0 | 0 | -15.3% | 0 |
| class CHEAP, legacy tier WATCHLIST | 2 | -22.5% | -22.8% to -22.5% | 0 | 0 | -17.6% | 0 |
| class FAIR, legacy tier ACCUMULATE | 5 | -3.1% | -23.2% to +9.3% | 0 | 0 | -9.1% | 0 |
| class FAIR, legacy tier WATCHLIST | 5 | -20.9% | -21.3% to +8.6% | 0 | 0 | -20.6% | 0 |
| class RICH, legacy tier AVOID | 3 | +3.1% | +2.2% to +5.0% | 0 | 0 | -9.5% | 3 |
| FY15E $1.045 (2016-01-08 to 2016-01-22) | 3 | +3.1% | +2.2% to +5.0% | 0 | 0 | -9.5% | 3 |
| FY16E $2.35 (2016-01-29 to 2016-04-22) | 13 | +7.4% | -23.2% to +15.2% | 0 | 0 | -7.7% | 0 |
| FY16E $2.42 (2016-04-29 to 2016-07-22) | 13 | -21.3% | -23.5% to -17.5% | 0 | 0 | -16.8% | 0 |
| FY16E $2.48 (2016-07-29 to 2016-10-21) | 13 | +14.8% | -19.7% to +21.9% | 0 | 0 | +6.7% | 0 |
| FY16E $2.67 (2016-10-28 to 2016-12-30) | 10 | +0.3% | -11.1% to +5.6% | 0 | 0 | +3.8% | 0 |
| latest print Q3 2015 (2016-01-08 to 2016-01-22) | 3 | +3.1% | +2.2% to +5.0% | 0 | 0 | -9.5% | 3 |
| latest print Q4 2015 (2016-01-29 to 2016-04-22) | 13 | +7.4% | -23.2% to +15.2% | 0 | 0 | -7.7% | 0 |
| latest print Q1 2016 (2016-04-29 to 2016-07-22) | 13 | -21.3% | -23.5% to -17.5% | 0 | 0 | -16.8% | 0 |
| latest print Q2 2016 (2016-07-29 to 2016-10-21) | 13 | +14.8% | -19.7% to +21.9% | 0 | 0 | +6.7% | 0 |
| latest print Q3 2016 (2016-10-28 to 2016-12-30) | 10 | +0.3% | -11.1% to +5.6% | 0 | 0 | +3.8% | 0 |

- **CHEAP held on none of 39 dates and FAIR on none of 10; RICH held on all 3.** The CHEAP dates ($49.77-74.81) returned -23.5% to
  +21.9% over two years and lagged SPY by 12.2-60.6pp; none cleared the hurdle. The FAIR dates ($62.16-76.00) returned -23.2% to +9.3%,
  30.1-55.3pp behind SPY, outside the ±15pp band. The three RICH dates of January (FY15E $1.045, $62.78-64.40) returned +2.2% to +5.0%
  and lagged SPY by 45.4-50.2pp, as RICH should.
- **The earnings arrived; the multiple did not hold.** FY2016 came in at $2.65 GAAP (the Q4 2016 release, 2017-01-26) against the
  $2.35-2.67 guides the 2016 models used. The price peaked at $76.77 on 2016-07-14 and fell to $46.82 on 2017-01-26, through one-day
  falls of 16.0% on 2016-08-05, 10.1% on 2016-10-10 and 11.3% on 2017-01-20. With hindsight, the first was the company's announcement that
  its trial of Opdivo alone in first-line non-small cell lung cancer (CheckMate -026) missed its primary endpoint; no such readout is in a
  model's inputs, and no point-in-time rule could have read it as a number.
- **The floor was a waypoint, not a support.** The EPP floor ($48.06-54.56) was reached within two years on every CHEAP and FAIR date. The
  two-year price landed nearest BASE on 42 dates (0.56-0.93 times the BASE price), BEAR on 7 (4.98-5.34 times BEAR) and BULL on the 3 RICH
  dates.
- **Three years did not repair it:** the CHEAP dates returned -33.0% to +20.4% to late 2019 (median -9.6%), none ahead of SPY.
- **The ranks were right within the year.** The entry price ranks the two-year return at -0.75 and the m12-24 return at -0.99, the EPP
  gap at -0.73 and -0.93, Ratio B at -0.70 and -0.93; the adjusted gap at +0.21 and +0.71 and the proxy composite at +0.04 and +0.56.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 16 | -5.6% | -9.0% to +9.2% | 0 | 0 | +1.0% | 0 |
| class CHEAP, legacy tier ACCUMULATE | 13 | -11.6% | -16.5% to -6.0% | 0 | 0 | -4.6% | 0 |
| class FAIR, legacy tier ACCUMULATE | 6 | -12.0% | -14.7% to -10.9% | 0 | 0 | -10.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 14 | -2.9% | -17.8% to +10.0% | 0 | 0 | -20.2% | 2 |
| class RICH, legacy tier AVOID | 3 | +1.2% | -4.8% to +7.5% | 0 | 0 | -20.8% | 3 |
| FY16E $2.67 (2017-01-06 to 2017-01-20) | 3 | -9.0% | -16.5% to +8.3% | 0 | 0 | +2.0% | 0 |
| FY17E $2.57 (2017-01-27 to 2017-04-21) | 13 | -5.6% | -8.9% to +9.2% | 0 | 0 | +0.2% | 0 |
| FY17E $2.795 (2017-04-28 to 2017-07-21) | 13 | -8.8% | -16.4% to -6.0% | 0 | 0 | -3.7% | 0 |
| FY17E $2.71 (2017-07-28 to 2017-10-20) | 13 | -14.7% | -17.8% to -10.9% | 0 | 0 | -20.2% | 0 |
| FY17E $2.41 (2017-10-27 to 2017-12-29) | 10 | +0.8% | -4.8% to +10.0% | 0 | 0 | -19.9% | 5 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | -9.0% | -16.5% to +8.3% | 0 | 0 | +2.0% | 0 |
| latest print Q4 2016 (2017-01-27 to 2017-04-21) | 13 | -5.6% | -8.9% to +9.2% | 0 | 0 | +0.2% | 0 |
| latest print Q1 2017 (2017-04-28 to 2017-07-21) | 13 | -8.8% | -16.4% to -6.0% | 0 | 0 | -3.7% | 0 |
| latest print Q2 2017 (2017-07-28 to 2017-10-20) | 13 | -14.7% | -17.8% to -10.9% | 0 | 0 | -20.2% | 0 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | +0.8% | -4.8% to +10.0% | 0 | 0 | -19.9% | 5 |

- **CHEAP held on none of 29 dates; FAIR on 2 of 20; RICH on all 3.** The CHEAP dates ($47.74-59.95) returned -16.5% to +9.2% over two
  years, 11.2-40.9pp behind SPY, none over the hurdle. The FAIR dates returned -17.8% to +10.0%; the two that held are the last two of the
  year (2017-12-22 and 2017-12-29, +9.5% and +10.0%, 14.4pp and 15.0pp behind SPY, just inside the band). The three RICH dates
  (2017-12-01 to 2017-12-15, $62.41-63.24) returned -4.8% to +7.5% and lagged SPY by 15.0-27.7pp.
- **The non-GAAP guide was met, GAAP fell to a tax charge, and the price fell anyway.** FY2017 came in at $3.01 non-GAAP, inside the last
  non-GAAP range ($2.95-3.05), and $0.61 GAAP (the Q4 2017 release of 2018-02-05, outside the series), after the tax-reform charges the
  8-K of 2018-01-05 first estimated at about $3 billion; the models used GAAP guides of $2.41-2.795. The two-year horizons end in 2019: the price fell 13.9% on 2019-01-03 (with hindsight, the day
  the company announced its agreement to acquire Celgene) and reached $42.77 on 2019-07-22. The floor ($45.79-50.73) was reached within two
  years on all 52 dates; the two-year price landed nearest BASE on 40 (0.57-1.03 times the BASE price) and BEAR on 12 (4.55-5.02 times).
- **Three years turned positive but not ahead:** the 2017 CHEAP dates returned -3.2% to +45.4% to late 2020 (median +19.6%), none ahead
  of SPY or over the three-year hurdle.
- **The ranks again ran through the price:** the entry price ranks the m12-24 return at -0.92 (the two-year return at -0.25), the EPP gap
  at -0.91, Ratio B at -0.95; the adjusted gap at +0.98 and the proxy composite at +0.85 on the m12-24 measure.

## Across 2014-2017

- **The call held on 74 of 209 dates:** RICH on 72 of 111 (13 of 52 in 2014, all 53 in 2015, 3 of 3 in January 2016, 3 of 3 in December
  2017), FAIR on 2 of 30, CHEAP on none of 68. With 2008-2013, the call held on 292 of 523 dates; CHEAP on 207 of 288.
- **The CHEAP calls of 2016-2017 failed on every date.** They rest on guides that were met (FY2016 $2.65 GAAP; FY2017 $3.01 non-GAAP, inside its last
  range, before a tax-reform charge took GAAP to $0.61), on BASE growth taken from one quarter's revenue growth during a launch (+18% to +24% ex-FX, so BASE +20% to +26%/yr for two
  years), and on a P/E window and floor lifted by the multiples of depressed earnings (2006-2007 and 2014; 2015's own days excluded). The
  market re-priced the pipeline instead: the stock fell 39-44% from its July 2016 high through trial and deal news that no fact sheet field carries.
  Hypothesis, not a rule: a BASE that extrapolates a single launch quarter's growth, against a window whose floor comes from trough-EPS
  years, calls CHEAP on a stock whose value moves on binary readouts; test it on other series and periods, never fit it to BMY or carry it
  into a BMY model.
- **The same rule that missed in early 2014 held in 2015.** RICH on GAAP guides cut by impairments and upfront payments, ranked against the
  stock's own multiples, lagged SPY from October 2014 to January 2016 (69 of 69 dates) after the dates of January to September 2014 had beaten
  it. With 2012-2013, RICH on trough GAAP earnings failed for about two years (July 2012 to September 2014) and then held for about
  sixteen months: a timing question no point-in-time input settles.
- **Unanimity tracked the RICH calls, not the CHEAP ones.** The 102 dates on which all eight robustness variants agreed held on 69 (86 RICH
  dates, 69 held; 16 CHEAP dates, none held); the 68 dates on seven of eight held on none. A label, not a filter.
- **The ranks ran through the price, and the composite turned useful only within 2016-2017.** Across the 209 dates the entry price ranks
  the two-year return at -0.69 and the m12-24 return at -0.86; the EPP gap at -0.17 and -0.28, the adjusted gap at +0.02 and +0.16, the
  proxy composite at +0.06 and +0.21. Within 2016-2017 the adjusted gap (+0.23 and +0.87) and the composite (+0.19 and +0.73) carry the
  right sign; across 2008-2017 the composite still carries no reliable sign.
- **2015's exclusion did not decide the outcome.** The sensitivity that keeps 2015 at GAAP turns 13 FAIR dates of 2016-2017 CHEAP and 3
  RICH dates of December 2017 FAIR; none of those 13 would have held as CHEAP (every 2016-2017 date lagged SPY and missed the hurdle), and
  the 3 RICH dates that held would have become FAIR dates 15.0-27.7pp behind SPY, two of them outside the band. Checked after scoring,
  as a label; the encoding stays as decided.


## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 10 | +25.1% | +21.7% to +31.4% | 0 | 0 | +16.5% | 0 |
| class CHEAP, legacy tier ACCUMULATE | 3 | +18.3% | +15.6% to +27.1% | 0 | 1 | +4.7% | 1 |
| class CHEAP, legacy tier WATCHLIST | 2 | +13.5% | +7.9% to +13.5% | 0 | 0 | +4.2% | 0 |
| class FAIR, legacy tier ACCUMULATE | 8 | +23.7% | +6.2% to +27.3% | 0 | 7 | +4.4% | 7 |
| class FAIR, legacy tier WATCHLIST | 26 | +5.6% | -19.9% to +12.4% | 0 | 0 | -4.1% | 16 |
| class RICH, legacy tier AVOID | 3 | +5.0% | +4.3% to +9.1% | 0 | 0 | -19.4% | 3 |
| FY17E $2.41 (2018-01-05 to 2018-02-02) | 5 | +6.8% | +4.3% to +12.4% | 0 | 0 | -18.8% | 4 |
| FY18E $3.075 (2018-02-06 to 2018-04-20) | 11 | +0.5% | -19.9% to +27.1% | 0 | 1 | -16.3% | 7 |
| FY18E $2.75 (2018-04-27 to 2018-07-20) | 13 | +19.8% | +6.6% to +27.3% | 0 | 7 | +3.2% | 12 |
| FY18E $2.73 (2018-07-27 to 2018-10-19) | 13 | +7.9% | -1.8% to +18.3% | 0 | 0 | -2.7% | 4 |
| FY18E $3.1 (2018-10-26 to 2018-12-28) | 10 | +25.1% | +21.7% to +31.4% | 0 | 0 | +16.5% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-02-02) | 5 | +6.8% | +4.3% to +12.4% | 0 | 0 | -18.8% | 4 |
| latest print Q4 2017 (2018-02-06 to 2018-04-20) | 11 | +0.5% | -19.9% to +27.1% | 0 | 1 | -16.3% | 7 |
| latest print Q1 2018 (2018-04-27 to 2018-07-20) | 13 | +19.8% | +6.6% to +27.3% | 0 | 7 | +3.2% | 12 |
| latest print Q2 2018 (2018-07-27 to 2018-10-19) | 13 | +7.9% | -1.8% to +18.3% | 0 | 0 | -2.7% | 4 |
| latest print Q3 2018 (2018-10-26 to 2018-12-28) | 10 | +25.1% | +21.7% to +31.4% | 0 | 0 | +16.5% | 0 |

- **FAIR held on 23 of 34, CHEAP on 1 of 15, RICH on all 3.** The FAIR dates ($51.33-68.96) returned -19.9% to +27.3% over two years
  against SPY's -9.3% to +27.5%; 23 landed within the ±15pp band. The CHEAP dates ($49.82-60.90, the two after the Q4 2017 print and
  the 13 on the Q3 2018 guide of $3.10, 15-17x) returned +7.9% to +31.4%, none over the hurdle and all but one behind SPY (by up to
  28.0pp): the stock fell 13.9% on 2019-01-03 and touched $42.77 on 2019-07-22 inside their horizons. The three RICH dates of January
  ($62.81-64.25) returned +4.3% to +9.1%, 12.0-16.3pp behind SPY.
- **The floor was reached on every date** ($45.79-55.35 against a two-year low of $42.77) and the two-year price landed nearest BASE on
  all 52 (BASE +3.1% to +12.1%/yr). Over three years (to late 2021) -6.4% to +39.3%, none ahead of SPY or over the three-year hurdle.
- **The ranks ran through the price:** the entry price ranks the two-year return at -0.89 and the m12-24 return at -0.95, the EPP gap at
  -0.65 and -0.68, Ratio B at -0.77 and -0.87; the adjusted gap at +0.61 and +0.82 and the proxy composite at +0.47 and +0.68.

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 48 | +41.7% | +2.6% to +61.6% | 30 | 8 | +27.5% | 30 |
| class CHEAP, legacy tier ACCUMULATE | 4 | +3.0% | -1.6% to +3.1% | 0 | 0 | -0.9% | 0 |
| FY18E $3.1 (2019-01-04 to 2019-01-18) | 3 | +39.8% | +38.4% to +42.7% | 3 | 0 | +26.3% | 3 |
| FY19E $3.8 (2019-01-25 to 2019-04-18) | 13 | +31.7% | +22.4% to +51.7% | 6 | 1 | +21.3% | 6 |
| FY19E $3.89 (2019-04-26 to 2019-07-19) | 13 | +51.4% | +38.0% to +61.6% | 13 | 5 | +31.9% | 13 |
| FY19E $3.78 (2019-07-26 to 2019-10-25) | 14 | +43.5% | +12.0% to +57.3% | 8 | 2 | +31.7% | 8 |
| FY19E $3.51 (2019-11-01 to 2019-12-27) | 9 | +3.1% | -1.6% to +9.2% | 0 | 0 | +8.2% | 0 |
| latest print Q3 2018 (2019-01-04 to 2019-01-18) | 3 | +39.8% | +38.4% to +42.7% | 3 | 0 | +26.3% | 3 |
| latest print Q4 2018 (2019-01-25 to 2019-04-18) | 13 | +31.7% | +22.4% to +51.7% | 6 | 1 | +21.3% | 6 |
| latest print Q1 2019 (2019-04-26 to 2019-07-19) | 13 | +51.4% | +38.0% to +61.6% | 13 | 5 | +31.9% | 13 |
| latest print Q2 2019 (2019-07-26 to 2019-10-25) | 14 | +43.5% | +12.0% to +57.3% | 8 | 2 | +31.7% | 8 |
| latest print Q3 2019 (2019-11-01 to 2019-12-27) | 9 | +3.1% | -1.6% to +9.2% | 0 | 0 | +8.2% | 0 |

- **CHEAP held on 30 of 52, all by clearing the hurdle.** The 43 dates to 2019-10-25 ($43.33-54.98, 11-16x the GAAP guides that
  excluded Celgene, all BUY) returned +12.0% to +61.6% over two years, and the 30 that held cleared the +32.2% hurdle; only 8 beat SPY,
  whose two years from 2019 ran +42.7% to +61.0% through the 2020 rebound. The Q1 2019-print dates, at the year's lowest prices
  ($43.33-49.34), returned +38.0% to +61.6%. The nine dates after the Q3 2019 print ($56.45-64.14, five BUY and four ACCUMULATE) returned
  -1.6% to +9.2%, 42-52pp behind SPY.
- **Three years made the call:** +22.4% to +86.0% to late 2022 (median +51.8%), 36 of 52 ahead of SPY and 25 over the three-year hurdle.
  The two-year price landed nearest BASE on 42 dates and BEAR on 10; the floor ($46.50-62.24) sat above the price from the Q4 2018 print
  to the Q2 2019 print and was reached or passed within two years on every date.
- **The ranks were nearly perfect within the year:** the entry price ranks both measures at -0.96, the EPP gap at -0.89 and -0.90,
  Ratio B at -0.89 and -0.88; the adjusted gap at +0.45 and +0.46, the proxy composite at +0.17 and +0.15.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 5 | +3.8% | +3.1% to +9.2% | 0 | 0 | -1.9% | 0 |
| class RICH, legacy tier AVOID | 48 | +29.9% | +5.7% to +54.7% | 19 | 27 | +13.2% | 14 |
| FY19E $3.51 (2020-01-03 to 2020-01-31) | 5 | +3.8% | +3.1% to +9.2% | 0 | 0 | -1.9% | 0 |
| FY20E $0.85 (2020-02-07 to 2020-05-01) | 13 | +31.4% | +5.7% to +54.7% | 6 | 0 | +7.4% | 7 |
| FY20E $0.47 (2020-05-08 to 2020-07-31) | 13 | +33.1% | +24.4% to +44.1% | 8 | 8 | +13.2% | 4 |
| FY20E $0.015 (2020-08-07 to 2020-10-30) | 13 | +25.8% | +19.4% to +38.5% | 1 | 10 | +13.3% | 3 |
| FY20E $0.52 (2020-11-06 to 2020-12-31) | 9 | +29.9% | +21.8% to +36.8% | 4 | 9 | +14.9% | 0 |
| latest print Q3 2019 (2020-01-03 to 2020-01-31) | 5 | +3.8% | +3.1% to +9.2% | 0 | 0 | -1.9% | 0 |
| latest print Q4 2019 (2020-02-07 to 2020-05-01) | 13 | +31.4% | +5.7% to +54.7% | 6 | 0 | +7.4% | 7 |
| latest print Q1 2020 (2020-05-08 to 2020-07-31) | 13 | +33.1% | +24.4% to +44.1% | 8 | 8 | +13.2% | 4 |
| latest print Q2 2020 (2020-08-07 to 2020-10-30) | 13 | +25.8% | +19.4% to +38.5% | 1 | 10 | +13.3% | 3 |
| latest print Q3 2020 (2020-11-06 to 2020-12-31) | 9 | +29.9% | +21.8% to +36.8% | 4 | 9 | +14.9% | 0 |

- **RICH held on 14 of 48; the label came from purchase accounting.** From the Q4 2019 print the models read the GAAP guides after
  the Celgene acquisition ($0.85, $0.47, $0.015, $0.52: 57-4,211x), and every date after the print is RICH. The stock ($48.40-66.38)
  returned +5.7% to +54.7% over two years; 27 beat SPY and 19 cleared the hurdle; the 14 that held lagged SPY's rebound from March 2020
  and missed the hurdle. The two-year price landed nearest BULL on 26 and XBULL on 21 (the scenario prices are multiples of those GAAP
  EPS figures). Over three years (to late 2023) -12.1% to +51.4%, behind SPY on 52 of 53.
- **The two sensitivities that undo the label would have scored better as labels** (checked after scoring; the encodings stay as
  decided): on the non-GAAP guides all 48 dates and the 4 of January 2021 were CHEAP, and 38 of those 52 cleared the hurdle or beat SPY,
  as CHEAP requires; on the reading of the Q2 2020 range as no numeric guide the 13 dates of August-October 2020 were CHEAP, and 10 of
  them beat SPY. The 5 CHEAP dates of January 2020 ($62.78-66.72, before the Q4 2019 print) returned +3.1% to +9.2%, 32-48pp behind SPY.
- **The ranks within the year carry little:** the entry price ranks the two-year return at -0.72 and the m12-24 return at -0.74; the
  EPP gap, the adjusted gap and Ratio B (15 finite dates) at -0.29 to +0.41, around zero or the wrong sign, as the GAAP figures put the
  floor at $0.28-16.15 and Ratio B at 3.1 to infinite.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 12 | +19.8% | +12.4% to +29.1% | 0 | 12 | +20.5% | 12 |
| class CHEAP, legacy tier ACCUMULATE | 6 | +5.7% | +4.0% to +13.8% | 0 | 6 | +17.2% | 6 |
| class CHEAP, legacy tier WATCHLIST | 15 | +3.2% | -4.4% to +12.4% | 0 | 7 | +12.3% | 7 |
| class FAIR, legacy tier WATCHLIST | 15 | -3.5% | -10.6% to +4.6% | 0 | 2 | +3.7% | 15 |
| class RICH, legacy tier AVOID | 4 | +23.5% | +15.3% to +24.8% | 0 | 4 | +16.9% | 0 |
| FY20E $0.52 (2021-01-08 to 2021-01-29) | 4 | +23.5% | +15.3% to +24.8% | 0 | 4 | +16.9% | 0 |
| FY21E $3.22 (2021-02-05 to 2021-04-23) | 12 | +19.8% | +12.4% to +29.1% | 0 | 12 | +20.5% | 12 |
| FY21E $3.28 (2021-04-30 to 2021-07-23) | 13 | +3.9% | -1.5% to +13.8% | 0 | 6 | +8.1% | 9 |
| FY21E $2.87 (2021-07-29 to 2021-10-22) | 13 | +3.2% | -4.8% to +6.7% | 0 | 7 | +9.7% | 13 |
| FY21E $2.755 (2021-10-28 to 2021-12-31) | 10 | -4.1% | -10.6% to -2.9% | 0 | 2 | +13.7% | 6 |
| latest print Q3 2020 (2021-01-08 to 2021-01-29) | 4 | +23.5% | +15.3% to +24.8% | 0 | 4 | +16.9% | 0 |
| latest print Q4 2020 (2021-02-05 to 2021-04-23) | 12 | +19.8% | +12.4% to +29.1% | 0 | 12 | +20.5% | 12 |
| latest print Q1 2021 (2021-04-30 to 2021-07-23) | 13 | +3.9% | -1.5% to +13.8% | 0 | 6 | +8.1% | 9 |
| latest print Q2 2021 (2021-07-29 to 2021-10-22) | 13 | +3.2% | -4.8% to +6.7% | 0 | 7 | +9.7% | 13 |
| latest print Q3 2021 (2021-10-28 to 2021-12-31) | 10 | -4.1% | -10.6% to -2.9% | 0 | 2 | +13.7% | 6 |

- **CHEAP held on 25 of 33, FAIR on all 15, RICH on none of 4.** The 12 CHEAP and BUY dates of the Q4 2020 print ($59.99-66.01, 19-21x
  FY21E $3.22) returned +12.4% to +29.1% over two years and beat SPY by up to 20.4pp; none cleared the hurdle. The CHEAP dates from the
  Q1 2021 print returned -4.4% to +13.8%, 13 of 21 ahead of SPY, whose two years from 2021 ran -7.6% to +9.5%. The FAIR dates returned
  -10.6% to +4.6%, all within the band. The four RICH dates of January 2021 (FY20E $0.52) returned +15.3% to +24.8% and beat SPY.
- **The level fell back after the first year:** the stock peaked at $81.13 on 2022-12-02 and fell to $48.48 on 2023-11-21 inside the
  horizons, so the two-year price landed nearest BASE on 36 dates and BEAR on 12; over three years (to late 2024) -30.4% to +16.4%, none
  ahead of SPY.
- **Ratio B ranked best:** -0.83 against the two-year return and -0.92 against the m12-24 return; the proxy composite +0.58 and +0.49;
  the entry price -0.07 and -0.69.

## Across 2018-2021

- **The call held on 111 of 209 dates:** CHEAP on 56 of 105, FAIR on 38 of 49, RICH on 17 of 55. With 2008-2017, the call held on 403
  of 732: CHEAP on 263 of 393, FAIR on 51 of 99, RICH on 89 of 240.
- **The 2020 RICH calls are a purchase-accounting artifact.** On GAAP EPS after the Celgene acquisition (amortization of acquired
  intangibles near $10 billion a year, the inventory step-up, the acquired IPRD) the models priced the stock at 57-4,211x; the market
  priced it on the company's figures and the stock rose. Hypothesis, not a rule: after a large acquisition, GAAP EPS stops measuring the
  earnings the market prices, and a P/E on it ranked against the pre-deal history flags RICH; test it on other acquirers and periods,
  never fit it to BMY or carry it into a BMY model. The method's rules (GAAP EPS where the adjusted figure removes recurring costs, the
  guide midpoint as published) produce this mechanically; changing them is a method question for the owner, with a full re-run.
- **The 2019 CHEAP calls held on the hurdle, not on SPY.** The GAAP guides that excluded Celgene put the stock at 11-15x against a
  pre-deal window; it returned +38% to +62% from the cheapest entries, but SPY's 2020-2021 run beat most of them over two years. Three
  years settled it in the model's favour (36 of 52 ahead of SPY).
- **Unanimity tracked the CHEAP calls this time.** The 88 dates on which all eight robustness variants agreed held on 56 (42 of 56 CHEAP,
  14 of 32 RICH); the 121 on seven or fewer held on 55. A label, not a filter (in 2014-2017 unanimity tracked only the RICH calls).
- **The ranks:** across the 209 dates the entry price ranks the two-year return at -0.67 and the m12-24 return at -0.67; the EPP gap at
  -0.18 and -0.50, the adjusted gap at +0.11 and +0.55, the proxy composite at +0.31 and +0.41: the right signs on the m12-24 measure,
  weak on the two-year one, with 2020's GAAP figures adding noise.
