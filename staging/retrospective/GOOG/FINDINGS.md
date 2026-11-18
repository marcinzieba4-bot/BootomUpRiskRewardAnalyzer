# GOOG retrospective findings (hindsight)

Patterns seen in `outcome.json` for the GOOG weekly dates: 522 in all, 105 from 2008-01-04 to 2009-12-31, 209 from 2010-01-08 to
2013-12-31 and 208 from 2014-01-10 to 2017-12-29: Google Inc. to 2015-10-02 and Alphabet Inc. after, the Class A common stock (NASDAQ:
GOOG) to 2014-03-26 and the Class C capital stock (Yahoo's GOOG series) from 2014-03-27. They are **labels and hypotheses**: never feed
them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and pushed
(2008-2009: f268b6d, firewall result 4d0926c; 2010-2013: 538c9a3, with the correction of two 2008-2009 vintage notes, firewall result
b0b6461; 2014-2017: 3ff288d, firewall result 9fa6d66); the outcomes were computed on 2026-11-18. Every date has its 6-month, 1-, 2- and
3-year horizons (the last ends 2020-12-29). Google paid no dividend in these horizons, so total returns are price returns. The horizons
that end after the 2014-04-02 distribution of one Class C share per Class A share (92 two-year horizons of 2010-2013, from the 2012-04-13
entry on, and the 11 entries of 2014-01-10 to 2014-03-21) are measured on Yahoo's GOOG series, which counts one Class A share as 2.002
Class C shares and the 2015 Adjustment Payment as 1.0027455 more; a holder's one A plus one C share was worth 0.1 to 3.2 points more over
two years for the 2010-2013 entries (no call changes) and 1.1 to 1.8 points more for the 2014 entries (one call changes: below). Medians
of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over
three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY); FAIR should land within 15 points of
the benchmark; RICH should miss the hurdle and lag the benchmark. Spearman ranks are given against the two-year return and the m12-24
average price return.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +3.6% | -18.7% to +125.1% | 15 | 51 | +7.8% | 51 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -4.6% | -5.8% to -3.4% | 0 | 4 | -24.8% | 4 |
| latest print Q4 2007 (2008-02-01 to 2008-04-11) | 11 | +20.7% | +0.7% to +32.3% | 1 | 11 | +5.4% | 11 |
| latest print Q1 2008 (2008-04-18 to 2008-07-11) | 13 | -12.4% | -18.7% to +2.0% | 0 | 11 | -6.8% | 11 |
| latest print Q2 2008 (2008-07-18 to 2008-10-10) | 13 | +3.6% | -5.8% to +61.6% | 2 | 13 | +14.1% | 13 |
| latest print Q3 2008 (2008-10-17 to 2008-12-31) | 12 | +94.6% | +61.4% to +125.1% | 12 | 12 | +72.8% | 12 |

- **CHEAP held on 51 of 53 dates, mostly by losing less than the market.** Every 2008 entry but two beat SPY over two years (SPY's own
  two-year return from those dates was -18.7% to +56.9%), but only 15 cleared the hurdle: 2008-03-14 ($437.92, +32.3%), 2008-10-03,
  2008-10-10 and the twelve from the Q3 2008 print to the end of the year ($262.43-372.54, +61.4% to +125.1%). The entries of January
  ($566-657) lost 3.4-5.8%; those of the Q1 2008 quarter ($528-586) lost up to 18.7%, and the two that missed, 2008-07-03 ($537.00,
  -18.7%) and 2008-07-11 ($533.80, -12.4%), lagged SPY by 3.3 points each. The 46 dates to 2008-11-14 all sat through the fall to the
  2008-11-24 close of $257.44, 17-61% below their entry prices. Over three years (to the end of 2011) the 2008 dates returned -11.7% to +121.4% (median +21.1%); 39 beat
  SPY and 13 cleared the three-year hurdle.
- **The anchor held up, and the earnings beyond it were much larger.** The models carried FY06's $9.94 in January, then FY07's $13.29;
  FY2008 came in at $13.31 (after the $1,094.8M equity impairment), and FY2009 at $20.41 a diluted share (the Q4 2009 release of
  2010-01-21, after the close). So the 2008-11-24 low, 19.4x FY07's $13.29 in the models, was 12.6x the year that followed, and the
  EPP floor ($437-452 from February) was passed by every 2008 date's two-year price but one ($436.55).
- **The ranks ran through the price, and every price-based metric had the right sign.** Across the 53 dates the entry price ranks the
  two-year return at Spearman -0.92 and the return to the m12-24 average price at -0.97; the EPP gap ranks them at -0.92 and -0.96, Ratio B
  at -0.91 and -0.97, the adjusted gap at +0.80 and +0.77 and the proxy composite at +0.69 and +0.49.
- **The two-year price landed nearest BEAR on 46 dates and BASE on 7.** BEAR was FY2002-FY2003's -8.9%/yr at the window's 10th-percentile
  multiple; the two-year prices ($436.55-626.75) were 0.44-0.76 times BASE, and none came within 0.13 times the BULL price.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 40 | +35.3% | -0.2% to +108.3% | 22 | 11 | +35.0% | 24 |
| class FAIR, legacy tier BUY | 10 | +6.3% | -2.9% to +11.9% | 0 | 0 | -0.7% | 9 |
| class RICH, legacy tier BUY | 2 | +4.2% | +2.4% to +4.2% | 0 | 0 | -8.1% | 2 |
| latest print Q3 2008 (2009-01-09 to 2009-01-16) | 2 | +108.3% | +95.7% to +108.3% | 2 | 2 | +78.9% | 2 |
| latest print Q4 2008 (2009-01-23 to 2009-04-09) | 12 | +77.5% | +55.2% to +94.6% | 12 | 6 | +59.1% | 12 |
| latest print Q1 2009 (2009-04-17 to 2009-07-10) | 13 | +28.4% | +11.7% to +38.2% | 5 | 0 | +34.3% | 5 |
| latest print Q2 2009 (2009-07-17 to 2009-10-09) | 13 | +13.4% | -0.2% to +38.9% | 3 | 3 | +21.4% | 5 |
| latest print Q3 2009 (2009-10-16 to 2009-12-31) | 12 | +6.3% | -2.9% to +11.9% | 0 | 0 | -1.1% | 11 |

- **CHEAP held on 24 of 40 dates; FAIR on 9 of 10 and RICH on both.** The 14 CHEAP entries to 2009-04-09 ($299.67-372.50) returned
  +55.2% to +108.3% and cleared the hurdle. From the Q1 2009 print the gains shrank as the price rose: the 16 misses are eight of the
  ten entries from 2009-05-08 to 2009-07-10 ($407-444, +11.7% to +31.4%, short of the hurdle and of SPY's own +38.9% to +58.0% from the
  same dates) and all eight from 2009-08-21 to 2009-10-09 ($461-516, -0.2% to +13.8%). The class turned to FAIR on the Q3 2009 print (2009-10-16)
  and to RICH on 2009-12-24; those twelve entries ($536-620) returned -2.9% to +11.9% and lagged SPY by 9.2-16.7 points, so FAIR missed
  only once (2009-10-30, 16.7 points behind) and RICH held on both. The two-year high was $626.77-645.90 (November 2010 to December
  2011). Over three years (to the end of 2012) the 2009 dates returned +12.9% to +108.6% (median +45.7%); 13 beat SPY and 21 cleared the
  three-year hurdle.
- **The ranks ran through the price again.** The entry price ranks the two-year return at Spearman -0.95 and the m12-24 average at -1.00;
  the EPP gap at -0.95 and -1.00, Ratio B at -0.93 and -0.99, the adjusted gap at +0.66 and +0.75 and the proxy composite at +0.48 and
  +0.62, all the right signs.
- **The two-year price landed nearest BASE on all 52 dates.** BASE carried the quarter's revenue growth less the dilution (+10.8%/yr on
  Q4 2008, -4.4% on Q2 2009, 0.0% on Q3 2009); the two-year prices were 0.76-1.30 times it and at most 0.19 times BULL.

## Across 2008-2009

- **The class moved once, late, and the tier never.** CHEAP on 93 dates, FAIR on 10 and RICH on 2, robust on all but the last two; the
  call held on 86 of 105 (CHEAP 75 of 93, FAIR 9 of 10, RICH 2 of 2). Across the 105 the entry price ranks the two-year return at
  Spearman -0.91 and the m12-24 average at -0.96, the EPP gap at -0.92 and -0.96, the adjusted gap at +0.70 and +0.76, Ratio B at -0.64
  and -0.68 and the proxy composite at +0.52 and +0.57. The legacy tier was BUY on every date: BULL and XBULL, the EPS CAGR from FY2001's
  $0.04 (+129% to +201%/yr) and FY2003-FY2005's +250%/yr, put the BULL price at $3,344-5,623 and Ratio B near zero whatever the price,
  and no two-year price came within a fifth of it.
- Hypotheses only, to test on other tickers and periods and never to fold into GOOG's method or fact sheet: (1) for a company whose
  decade is its start-up and hypergrowth, the r2 BULL and XBULL rules read the growth of a $0.04 year forward, so Ratio B and the legacy
  tier carry no information, and only the EPP gap, the adjusted gap and the class rank the outcomes; (2) rule T over the same years puts
  revenue growth at BEAR on every date, so the composite moves only with the margin and receivables signals; it still ranked both years
  the right way, unlike MU's 2009; (3) the turn to FAIR and RICH in late 2009 came from the conservative case (BASE falling to zero as
  revenue growth met the dilution) with the price 25-41% above a floor of the stock's own post-listing lows, and those entries lagged the
  market by 9-17 points over two years.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 50 | +17.9% | +4.4% to +47.2% | 10 | 14 | +9.8% | 15 |
| class FAIR, legacy tier BUY | 2 | +8.0% | +7.8% to +8.0% | 0 | 0 | -1.8% | 2 |
| latest print Q3 2009 (2010-01-08 to 2010-01-15) | 2 | +8.0% | +7.8% to +8.0% | 0 | 0 | -1.8% | 2 |
| latest print Q4 2009 (2010-01-22 to 2010-04-09) | 12 | +12.2% | +4.4% to +15.8% | 0 | 0 | +3.6% | 0 |
| latest print Q1 2010 (2010-04-16 to 2010-07-09) | 13 | +18.6% | +9.7% to +33.0% | 1 | 1 | +17.4% | 2 |
| latest print Q2 2010 (2010-07-16 to 2010-10-08) | 13 | +42.1% | +25.1% to +47.2% | 9 | 9 | +22.1% | 9 |
| latest print Q3 2010 (2010-10-15 to 2010-12-31) | 12 | +15.7% | +9.3% to +23.2% | 0 | 4 | +7.3% | 4 |

- **CHEAP held on 15 of 50 dates: every 2010 entry made money, most less than the market.** The two-year returns were +4.4% to +47.2%,
  while SPY returned +15.9% to +38.6% from the same dates; ten cleared the hurdle, nine of them entries of the Q2 2010 print ($459-536,
  July to October) and one of the Q1 2010 print. The 35 misses are the twelve of the Q4 2009 print (+4.4% to +15.8%, 8-19 points behind SPY), eleven of the Q1
  2010 print, the first four of the Q2 2010 print (+25.1% to +30.4%, at most 6.7 points behind) and eight of the Q3 2010 print ($590-625).
  The two FAIR dates of January 2010 held (+7.8%, +8.0%, within 15 points of SPY). Over three years (to the end of 2013) the 2010 dates
  returned +21.8% to +102.1% (median +73.5%); 44 beat SPY and 35 cleared the three-year hurdle.
- **The earnings came; the multiple fell.** The anchors were FY09's $20.41 and, from 2011-01-21, FY10's $26.31; FY2010 came in at $26.31
  and FY2011 at $29.76 (+29% and +13%), while the price two years on ($561-762) was 0.53-1.24 times the BASE price. The two-year price
  landed nearest BEAR on 42 dates, and above the EPP floor ($633-674) on only 18.
- **Within the year the price ranked the outcomes; the composite had the wrong sign.** The entry price ranks the two-year return at
  Spearman -0.68 and the m12-24 average at -0.86, the EPP gap at -0.70 and -0.88, Ratio B at -0.70 and -0.86; the adjusted gap at -0.00
  and -0.10 (none) and the proxy composite at -0.47 and -0.57.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +64.4% | +15.1% to +85.8% | 44 | 49 | +36.8% | 49 |
| latest print Q3 2010 (2011-01-07 to 2011-01-14) | 2 | +19.2% | +15.9% to +19.2% | 0 | 0 | +4.5% | 0 |
| latest print Q4 2010 (2011-01-21 to 2011-04-08) | 12 | +34.0% | +15.1% to +44.8% | 6 | 11 | +11.2% | 11 |
| latest print Q1 2011 (2011-04-15 to 2011-07-08) | 13 | +67.7% | +47.3% to +83.2% | 13 | 13 | +37.7% | 13 |
| latest print Q2 2011 (2011-07-15 to 2011-10-07) | 13 | +62.4% | +46.1% to +76.3% | 13 | 13 | +49.7% | 13 |
| latest print Q3 2011 (2011-10-14 to 2011-12-30) | 12 | +71.8% | +48.1% to +85.8% | 12 | 12 | +37.8% | 12 |

- **CHEAP held on 49 of 52.** The three misses are the first three weeks of the year ($612-624, +15.1% to +19.2%, 0.1-4.8 points behind
  SPY); from 2011-01-28 every entry beat SPY or cleared the hurdle, and from the Q1 2011 print ($475-646) all 38 cleared it (+46.1% to
  +85.8%). The 2011 low, $474.88 on 2011-06-24, was 18.0x FY10's $26.31, the series' lowest multiple of the period. Over three years (to
  the end of 2014) the 2011 dates returned +58.4% to +139.3% (median +95.9%); all 52 cleared the three-year hurdle and 47 beat SPY.
- **The ranks weakened as the whole year paid.** The entry price ranks the two-year return at -0.40 and the m12-24 average at -0.63, the
  EPP gap at -0.32 and -0.55, Ratio B at -0.45 and -0.63; the adjusted gap at +0.21 and +0.08 and the proxy composite at +0.25 and +0.01.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +74.8% | +44.5% to +102.4% | 52 | 50 | +60.6% | 52 |
| latest print Q3 2011 (2012-01-06 to 2012-01-13) | 2 | +79.7% | +71.9% to +79.7% | 2 | 2 | +43.5% | 2 |
| latest print Q4 2011 (2012-01-20 to 2012-04-05) | 12 | +93.6% | +72.0% to +102.4% | 12 | 12 | +54.3% | 12 |
| latest print Q1 2012 (2012-04-13 to 2012-07-13) | 14 | +91.9% | +68.0% to +101.1% | 14 | 14 | +76.4% | 14 |
| latest print Q2 2012 (2012-07-20 to 2012-10-12) | 13 | +67.0% | +46.4% to +95.0% | 13 | 13 | +58.5% | 13 |
| latest print Q3 2012 (2012-10-19 to 2012-12-28) | 11 | +55.3% | +44.5% to +68.4% | 11 | 9 | +64.3% | 11 |

- **CHEAP held on all 52, every entry clearing the hurdle** (+44.5% to +102.4%); 50 beat SPY (+34.3% to +55.5% from the same dates).
  The best were the Q4 2011 and Q1 2012 prints' entries ($565-643, 19.0-21.6x FY11's $29.76). Over three years (to the end of 2015) the
  2012 dates returned +54.6% to +127.2% (median +81.9%); all cleared the three-year hurdle and 50 beat SPY.
- **The two-year price landed nearest BASE on 41 dates**, 0.55-0.81 times the BASE price ($1,023-1,216 against BASE prices carried by
  +20-41%/yr revenue growth, Motorola's included); no two-year price came within 0.38 times BULL.
- **The price ranked the two-year return again** (-0.87; the m12-24 average -0.50), the EPP gap -0.84 and -0.41, Ratio B -0.87 and
  -0.39; the adjusted gap +0.50 and +0.37 and the proxy composite +0.37 and +0.47, the right signs.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 47 | +38.4% | +15.3% to +53.9% | 34 | 24 | +27.3% | 35 |
| class FAIR, legacy tier BUY | 6 | +39.8% | +34.3% to +43.9% | 6 | 6 | +9.9% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-01-18) | 3 | +42.4% | +34.2% to +44.4% | 3 | 1 | +52.3% | 3 |
| latest print Q4 2012 (2013-01-24 to 2013-04-12) | 12 | +38.0% | +34.6% to +43.3% | 12 | 3 | +39.3% | 12 |
| latest print Q1 2013 (2013-04-19 to 2013-07-12) | 13 | +22.3% | +15.3% to +41.2% | 1 | 1 | +25.2% | 1 |
| latest print Q2 2013 (2013-07-19 to 2013-10-11) | 13 | +41.4% | +37.1% to +53.9% | 13 | 13 | +26.3% | 13 |
| latest print Q3 2013 (2013-10-18 to 2013-12-31) | 12 | +39.3% | +31.4% to +47.2% | 11 | 12 | +11.3% | 6 |

- **CHEAP held on 35 of 47; FAIR missed on all 6.** The CHEAP misses are twelve of the thirteen entries of the Q1 2013 print ($800-923,
  April to July: +15.3% to +31.2%, short of the hurdle and 7-15 points behind SPY). The six FAIR entries of 2013-11-29 to 2013-12-31
  ($1,060-1,121, 63-73% over the floor) returned +34.3% to +43.9% and beat SPY by 18-24 points: the call expected the market's return
  within 15 points and got much more. FY2013 came in at $36.05 a diluted share from continuing operations (+11% on FY12's $32.46; the Q4
  2013 release of 2014-01-30, after the close). Over three years (to the end of 2016) the 2013 dates returned +38.3% to +101.8% (median
  +70.7%); all 53 beat SPY and 45 cleared the three-year hurdle.
- **The m12-24 average ranked by the entry price almost exactly** (Spearman -0.99, the EPP gap -0.99, Ratio B -0.85, the adjusted gap
  +0.87), while the two-year point return did not (+0.01): the two-year ends fell before and after the stock's jump of July 2015.

## Across 2010-2013

- **The class stayed CHEAP while the stock more than doubled, and it held on 153 of 209 dates** (CHEAP 151 of 201, FAIR 2 of 8): the
  anchor rose with each year's EPS ($20.41 to $32.46) and the window's median multiple fell toward the post-2008 years, so the price, from
  $437 to $1,121, stayed at the 5th-71st percentile of its own range. Every 2010-2013 entry made money over two years (+4.4% to +102.4%,
  median +44.8%); 146 cleared the hurdle and 143 beat SPY. Over three years 194 beat SPY and 184 cleared the hurdle.
- **The misses cluster where the market ran harder:** 2010 (35, SPY +16% to +39%), the first three weeks of 2011, the Q1 2013 print's
  entries and the late-2013 FAIR dates. Across the four years no point-in-time measure ranks the outcomes (the entry price -0.03 and +0.04,
  the EPP gap +0.04 and +0.12, the adjusted gap -0.05 and -0.19, the proxy composite -0.37 and -0.51): within a year the entry price did,
  as in 2008-2009, but the level moved with the earnings.
- Hypotheses only, to test on other tickers and periods and never to fold into GOOG's method or fact sheet: (1) when the anchor is the
  last reported year and earnings keep growing, a CHEAP class can persist for years without a timing signal, and its misses are relative
  (positive returns behind a strong market) rather than losses; (2) the FAIR turn of late 2013 came from BASE falling to the quarter's
  +11.9% revenue growth less the dilution while EPS grew faster than revenue, and those entries beat the market by 18-24 points; (3) the
  composite had the wrong sign in 2010 and 2013 and the right one in 2011-2012, so its sign is not stable for this ticker.

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class CHEAP, legacy tier BUY | 46 | +34.7% | +14.9% to +54.2% | 27 | 46 | +24.2% | 46 |
| class FAIR, legacy tier BUY | 5 | +21.2% | +13.9% to +29.6% | 0 | 5 | +6.6% | 3 |
| latest print Q3 2013 (2014-01-10 to 2014-01-24) | 3 | +26.9% | +21.2% to +29.6% | 0 | 3 | +7.8% | 1 |
| latest print Q4 2013 (2014-01-31 to 2014-04-11) | 11 | +25.0% | +13.9% to +39.1% | 2 | 11 | +6.1% | 11 |
| latest print Q1 2014 (2014-04-17 to 2014-07-11) | 13 | +30.6% | +16.1% to +42.0% | 5 | 13 | +22.6% | 13 |
| latest print Q2 2014 (2014-07-18 to 2014-10-10) | 13 | +34.5% | +23.6% to +44.7% | 9 | 13 | +24.5% | 13 |
| latest print Q3 2014 (2014-10-17 to 2014-12-26) | 11 | +45.6% | +35.6% to +54.2% | 11 | 11 | +38.2% | 11 |

- **CHEAP held on all 46 and every entry beat SPY** (+14.9% to +54.2% against SPY's +6.2% to +17.9%, by 4.1 to 40.8 points); 27 cleared
  the hurdle, the 19 that did not being entries of 2014-01-31 to 2014-09-19 ($552-1,216 as priced: the Class A before the split, the Class C
  from 2014-03-27). Of the five FAIR dates (January and February, on the Q3 2013 print and then the FY2013 10-K's lower BASE), three held and
  two missed upward: 2014-01-10 and 2014-01-24 beat SPY by 18.3 and 18.6 points. On a Class A holder's A plus C package the FAIR entry of
  2014-01-17 would miss too (+15.6 points over SPY instead of +14.5). The two-year price landed nearest BASE on all 51 (0.97-1.38 times
  the BASE price) and above the EPP floor on all. Over three years (to the end of 2017) the 2014 dates returned +35.9% to +107.9% (median
  +62.4%); all beat SPY and 39 cleared the three-year hurdle.
- **The entry price ranked the outcomes:** Spearman -0.84 against the two-year return and -0.85 against the m12-24 average, the EPP gap
  -0.83 and -0.80, Ratio B -0.65 and -0.55, the adjusted gap +0.65 and +0.57 (the composite was 1.95 on every date).

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class CHEAP, legacy tier BUY | 23 | +60.2% | +47.5% to +84.4% | 23 | 23 | +45.3% | 23 |
| class FAIR, legacy tier BUY | 18 | +50.5% | +40.4% to +74.4% | 18 | 18 | +36.3% | 1 |
| class RICH, legacy tier BUY | 1 | +49.8% | +49.8% to +49.8% | 1 | 1 | +31.4% | 0 |
| class RICH, legacy tier ACCUMULATE | 10 | +40.9% | +34.6% to +45.7% | 10 | 10 | +22.8% | 0 |
| class RICH, legacy tier WATCHLIST | 1 | +30.2% | +30.2% to +30.2% | 0 | 0 | +17.7% | 1 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +59.4% | +47.5% to +63.0% | 4 | 4 | +47.3% | 4 |
| latest print Q4 2014 (2015-01-30 to 2015-04-17) | 12 | +51.8% | +46.2% to +60.2% | 12 | 12 | +40.7% | 9 |
| latest print Q1 2015 (2015-04-24 to 2015-07-10) | 12 | +75.5% | +53.1% to +84.4% | 12 | 12 | +50.0% | 10 |
| latest print Q2 2015 (2015-07-17 to 2015-10-16) | 14 | +49.8% | +40.4% to +57.2% | 14 | 14 | +34.6% | 1 |
| latest print Q3 2015 (2015-10-23 to 2015-12-31) | 11 | +40.5% | +30.2% to +45.7% | 10 | 10 | +22.6% | 1 |

- **CHEAP held on all 23, FAIR on 1 of 18, RICH on 1 of 12: every miss was an upside miss.** The CHEAP entries ($496-549, January to June)
  returned +47.5% to +84.4% and beat SPY by 32.0 to 63.9 points. The FAIR entries ($540-673) returned +40.4% to +74.4% and beat SPY by 12.9
  to 57.8 points, so 17 fell outside the 15-point band on the upside (only 2015-09-18 held). The RICH entries of 2015-10-16 to 2015-12-31
  ($662-767, after the Q3 2015 print) returned +30.2% to +49.8%; only 2015-12-04 lagged SPY (by 0.2 points, +30.2%, short of the hurdle)
  and held, the other eleven cleared the hurdle and beat SPY by 2.4 to 19.7 points. The two-year price landed nearest BULL on 35 dates
  and BASE on 18. Over three years the 2015 dates returned +30.4% to +123.6% (median +95.0%); all beat SPY and 43 cleared the hurdle.
- **The price ranked the outcomes again** (-0.83 and -0.95), the EPP gap -0.86 and -0.93, Ratio B -0.77 and -0.89, the adjusted gap +0.76
  and +0.88; the proxy composite -0.67 and -0.69, the wrong sign.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class RICH, legacy tier BUY | 9 | +56.2% | +48.6% to +71.1% | 9 | 9 | +37.1% | 0 |
| class RICH, legacy tier ACCUMULATE | 23 | +54.0% | +35.6% to +65.1% | 23 | 23 | +40.8% | 0 |
| class RICH, legacy tier WATCHLIST | 20 | +48.2% | +24.0% to +61.1% | 17 | 20 | +41.0% | 0 |
| latest print Q3 2015 (2016-01-08 to 2016-01-29) | 4 | +59.4% | +54.9% to +61.6% | 4 | 4 | +29.8% | 0 |
| latest print Q4 2015 (2016-02-03 to 2016-04-15) | 11 | +53.0% | +35.6% to +62.2% | 11 | 11 | +34.4% | 0 |
| latest print Q1 2016 (2016-04-22 to 2016-07-22) | 14 | +55.8% | +46.8% to +71.1% | 14 | 14 | +42.9% | 0 |
| latest print Q2 2016 (2016-07-29 to 2016-10-21) | 13 | +53.5% | +37.2% to +61.1% | 13 | 13 | +39.7% | 0 |
| latest print Q3 2016 (2016-10-28 to 2016-12-30) | 10 | +34.7% | +24.0% to +45.8% | 7 | 10 | +45.9% | 0 |

- **RICH on all 52 and held on none: every entry beat SPY** (+24.0% to +71.1% against SPY's +11.0% to +53.3%, by 3.5 to 31.2 points) and
  49 cleared the hurdle (the three that did not, 2016-12-09 to 2016-12-23, returned +24.0% to +31.8% and still beat SPY). The class rested
  on a multiple at the 62nd-84th percentile of a window whose median had fallen to 23x, and on a conservative case of -18.7% to +8.0% over two years; FY15's $24.34
  (the Class C's, with the Adjustment Payment) gave way to FY2016's $27.85 (+14%). The two-year price landed nearest BULL on all 52
  (1.23-1.81 times BASE). Over three years the 2016 dates returned +42.8% to +85.8% (median +59.6%); 51 beat SPY and 44 cleared the hurdle.
- **The tiers inside RICH ordered the returns** (BUY median +56.2%, ACCUMULATE +54.0%, WATCHLIST +48.2%), but the ranks were weak: the price
  -0.53 and -0.09, the EPP gap -0.32 and -0.33, Ratio B -0.49 and +0.05, the adjusted gap +0.59 and -0.18, the composite +0.27 and -0.44.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class FAIR, legacy tier ACCUMULATE | 1 | +38.6% | +38.6% to +38.6% | 1 | 1 | +38.3% | 0 |
| class RICH, legacy tier ACCUMULATE | 11 | +37.6% | +32.5% to +48.0% | 11 | 11 | +34.7% | 0 |
| class RICH, legacy tier WATCHLIST | 7 | +32.8% | +18.9% to +40.4% | 4 | 5 | +30.5% | 2 |
| class RICH, legacy tier AVOID | 33 | +26.7% | +12.2% to +34.7% | 2 | 26 | +17.7% | 7 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +32.8% | +30.9% to +36.4% | 2 | 3 | +38.0% | 0 |
| latest print Q4 2016 (2017-01-27 to 2017-04-21) | 13 | +38.6% | +32.5% to +48.0% | 13 | 13 | +34.7% | 0 |
| latest print Q1 2017 (2017-04-28 to 2017-07-21) | 13 | +18.9% | +12.2% to +40.4% | 1 | 4 | +21.1% | 9 |
| latest print Q2 2017 (2017-07-26 to 2017-10-20) | 13 | +28.7% | +22.8% to +34.7% | 2 | 13 | +21.9% | 0 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | +27.6% | +23.4% to +31.0% | 0 | 10 | +11.9% | 0 |

- **RICH held on 9 of 51, the FAIR date (2017-02-03) missed upward.** The entries of the Q4 2016 print ($801-852, January to April)
  returned +32.5% to +48.0% and beat SPY by 11.9 to 24.3 points. The calls held from the Q1 2017 print: the entries of 2017-05-26 to
  2017-07-21 ($909-976, AVOID or WATCHLIST, 32.6-35.0x FY16's $27.85) returned +12.2% to +23.2% and lagged SPY by 3.8 to 10.1 points,
  short of the hurdle; the later Q2 and Q3 2017 entries ($911-1,064) returned +22.8% to +34.7% and beat SPY again by 0.9 to 10.2 points.
  The AVOID tier (33 dates from 2017-05-05) returned a median +26.7%, cleared the hurdle twice and beat SPY 26 times. Over three years (to
  the end of 2020) the 2017 dates returned +31.4% to +85.4% (median +59.8%); all beat SPY and 37 cleared the hurdle.
- **The m12-24 average ranked by the entry price almost exactly** (-0.99; the EPP gap -0.94, Ratio B -0.97, the adjusted gap +0.84), the
  two-year return less so (-0.67, -0.67, -0.66, +0.51); the composite +0.05 and +0.41.

## Across 2014-2017

- **Every entry made money and almost every one beat the market,** so the calls held where they expected gains and missed where they did
  not: over two years +12.2% to +84.4% (median +40.5%), 198 of 208 beat SPY and 146 cleared the hurdle; over three years 207 beat SPY. The
  call held on 83: CHEAP 69 of 69, FAIR 4 of 24 (every miss above the band), RICH 10 of 115 (one in December 2015, nine in May to July
  2017). The ten entries that lagged SPY are those ten.
- **The classes ordered the excess return, not the return:** median two-year excess over SPY +26.1 points for CHEAP, +20.7 for FAIR and
  +9.8 for RICH, while the median returns were +42.0%, +48.0% and +38.0%. The legacy tier ordered both: BUY (102 dates) +46.3% and +22.5
  points, ACCUMULATE (45) +45.7% and +13.5, WATCHLIST (28) +39.0% and +12.4, AVOID (33) +26.7% and +3.8. Across the four years the EPP gap
  ranks the outcomes best (-0.67 and -0.74), then the entry price (-0.59 and -0.55); Ratio B -0.36 and -0.27, the adjusted gap +0.25 and
  +0.16, the composite -0.12 and -0.33.
- Hypotheses only, to test on other tickers and periods and never to fold into GOOG's method or fact sheet: (1) a RICH class built on a
  multiple ranked against a window whose median falls as cheap post-crisis years enter it says little about a company compounding EPS
  at 12-23% a year: the 2016-2017 RICH entries still beat the market by a median of about 10 points; (2) as BULL and XBULL lost the
  start-up years, the legacy tier became informative (its four levels ordered both return and excess), unlike 2008-2013 when it was BUY
  throughout; (3) the FAIR misses were all upside misses, as in late 2013, so for this ticker FAIR behaved like a weaker CHEAP; (4) the
  composite's sign changed from year to year again (wrong in 2015, flat in 2014, mixed in 2016-2017).
