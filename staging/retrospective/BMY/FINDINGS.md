# BMY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the BMY weekly dates: 105 from 2008-01-04 to 2009-12-31, all Bristol-Myers Squibb Company (NYSE: BMY).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 4821356, firewall result 36e19d3); the outcomes were computed on 2026-11-12
and held unread until then. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31). Total returns include the
quarterly dividends ($0.31 from the ex-date of 2008-01-02, $0.32 from 2009-12-30, $0.33 from 2011-01-05, $0.34 from 2012-01-04); the
$0.32 rate was declared in December 2009 but stated in no filing of 2009, so the models of 2009-12-24 and 2009-12-31 carry $0.31 (checked
after scoring; no model changes). No split falls in any horizon, so every price is as traded; the Mead Johnson split-off of 2009-12-23
was an exchange offer, so a holder who did not tender kept the same shares and Yahoo's series needs no factor. Medians of an even count
take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the benchmark, and RICH
should miss the hurdle and lag the benchmark.

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

## Across both years

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
