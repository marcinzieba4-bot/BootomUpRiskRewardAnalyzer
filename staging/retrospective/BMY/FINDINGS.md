# BMY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the BMY weekly dates: 314 from 2008-01-04 to 2013-12-31, all Bristol-Myers Squibb Company (NYSE: BMY).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 4821356, firewall result 36e19d3; 2010-2013: 31cea6e, controls and firewall
result 533d892); the outcomes were computed on 2026-11-12. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends
2016-12-30). Total returns include the quarterly dividends ($0.31 from the ex-date of 2008-01-02, $0.32 from 2009-12-30, $0.33 from
2011-01-05, $0.34 from 2012-01-04, $0.35 from 2013-01-02, $0.36 from 2013-12-31, $0.37 from 2014-12-30, $0.38 from 2015-12-30). Each
December's new rate was stated in no filing before the next 10-K, so the models from the declaration to the 10-K carry the old rate ($0.31
from 2009-12-24 to 2010-02-12, $0.32 to 2011-02-11, and likewise later; $0.35 on 2013-12-31; checked after scoring; no model changes). No
split falls in any horizon, so every price is as traded; the Mead Johnson split-off of 2009-12-23 was an exchange offer, so a holder who
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
