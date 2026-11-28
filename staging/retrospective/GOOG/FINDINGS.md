# GOOG retrospective findings (hindsight)

Patterns seen in `outcome.json` for the GOOG weekly dates: 985 in all, 105 from 2008-01-04 to 2009-12-31, 209 from 2010-01-08 to
2013-12-31, 208 from 2014-01-10 to 2017-12-29, 209 from 2018-01-05 to 2021-12-31 and 254 from 2022-01-07 to 2026-11-13: Google Inc. to 2015-10-02 and Alphabet Inc. after, the Class A common stock (NASDAQ:
GOOG) to 2014-03-26 and the Class C capital stock (Yahoo's GOOG series) from 2014-03-27. They are **labels and hypotheses**: never feed
them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and pushed
(2008-2009: f268b6d, firewall result 4d0926c; 2010-2013: 538c9a3, with the correction of two 2008-2009 vintage notes, firewall result
b0b6461; 2014-2017: 3ff288d, firewall result 9fa6d66; 2018-2021: 120794a, firewall result 6985667; 2022-2026: 522c8f6, firewall result
a3a7ca3); the outcomes were computed on 2026-11-18 and (2018-2026) 2026-11-19. The dates to 2021 have their 6-month, 1-, 2- and 3-year
horizons; of 2022-2026, the two-year horizon exists for the 150 dates to 2024-11-15, the one-year for 202 to 2025-11-14 and the six-month
for 228 to 2026-05-15, and the 26 latest dates have none yet. Alphabet paid no dividend before June 2024; total returns include the
dividends from then. The 2022 twenty-for-one split changes no return (Yahoo's series is split-adjusted; the horizon prices are on each
entry's own share basis). The horizons
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

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class RICH, legacy tier AVOID | 52 | +29.0% | -4.5% to +77.6% | 16 | 51 | +16.1% | 1 |
| latest print Q3 2017 (2018-01-05 to 2018-01-26) | 4 | +27.4% | +23.4% to +30.1% | 0 | 4 | +6.8% | 0 |
| latest print Q4 2017 (2018-02-02 to 2018-04-20) | 12 | +18.3% | -4.5% to +42.5% | 2 | 12 | +16.1% | 0 |
| latest print Q1 2018 (2018-04-25 to 2018-07-20) | 13 | +27.8% | +23.2% to +32.1% | 0 | 13 | +14.0% | 0 |
| latest print Q2 2018 (2018-07-25 to 2018-10-19) | 13 | +28.4% | +19.6% to +41.4% | 4 | 12 | +15.6% | 1 |
| latest print Q3 2018 (2018-10-26 to 2018-12-28) | 10 | +68.9% | +48.4% to +77.6% | 10 | 10 | +40.3% | 0 |

- **RICH on every date, AVOID throughout, and the call held once:** the entries ($980-1,264) returned -4.5% to +77.6% over two years and beat
  SPY on 51 (by up to 33.7 points; SPY itself returned -9.3% to +57.5%, the two-year ends falling either side of the 2020 fall). Only
  2018-08-10 lagged (+20.9%, 1.6 points behind). The anchor was FY17's $18.00, the Tax Act year at GAAP; FY2018 came in at $43.70. The
  entries of the Q3 2018 print (October to December, $980-1,094) returned +48.4% to +77.6%. The two-year price landed
  nearest XBULL on 43 dates and BULL on 9; over three years the 2018 dates returned +55.6% to +194.5% (median +123.2%), all beating SPY and
  clearing the three-year hurdle.
- **Ranks:** the entry price -0.29 against the two-year return and -0.76 against the m12-24 average, the EPP gap -0.25 and -0.44, Ratio B
  +0.11 and +0.44, the adjusted gap +0.50 and +0.58, the composite +0.45 and +0.41.

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class FAIR, legacy tier WATCHLIST | 12 | +88.9% | +74.5% to +134.7% | 12 | 12 | +39.1% | 0 |
| class RICH, legacy tier WATCHLIST | 14 | +127.5% | +69.1% to +145.1% | 14 | 14 | +67.9% | 0 |
| class RICH, legacy tier AVOID | 26 | +123.4% | +58.1% to +140.3% | 26 | 26 | +78.5% | 0 |
| latest print Q3 2018 (2019-01-04 to 2019-02-01) | 5 | +67.1% | +58.1% to +74.1% | 5 | 5 | +37.8% | 0 |
| latest print Q4 2018 (2019-02-06 to 2019-04-26) | 12 | +84.4% | +69.1% to +88.9% | 12 | 12 | +36.5% | 0 |
| latest print Q1 2019 (2019-05-01 to 2019-07-19) | 12 | +127.5% | +99.7% to +134.7% | 12 | 12 | +67.9% | 0 |
| latest print Q2 2019 (2019-07-26 to 2019-10-25) | 14 | +131.0% | +119.4% to +145.1% | 14 | 14 | +75.9% | 0 |
| latest print Q3 2019 (2019-10-30 to 2019-12-27) | 9 | +123.8% | +111.0% to +135.1% | 9 | 9 | +83.3% | 0 |

- **No call held: FAIR and RICH entries alike more than doubled with the market's run into 2021.** The entries returned +58.1% to +145.1%
  and beat SPY by 10.8 to 86.4 points; every one cleared the hurdle. The twelve FAIR dates (2019-02-06 to 2019-06-28, $1,066-1,184 on FY18's
  $43.70) returned +74.5% to +134.7%, the 40 RICH +58.1% to +145.1%: the class did not separate them. The two-year price landed nearest
  XBULL on all 52 (1.35-3.03 times BASE; XBULL then +25.3%/yr). Over three years +30.1% to +169.8% (median +99.4%), all beating SPY.
- **Ranks:** the entry price +0.20 and +0.52 (the wrong sign), the EPP gap -0.69 and -0.30, Ratio B -0.14 and +0.32, the adjusted gap +0.09
  and -0.35, the composite -0.56 and -0.41.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class FAIR, legacy tier ACCUMULATE | 3 | +155.2% | +154.8% to +156.3% | 3 | 3 | +145.1% | 0 |
| class FAIR, legacy tier WATCHLIST | 4 | +113.9% | +87.0% to +121.2% | 4 | 4 | +117.5% | 0 |
| class RICH, legacy tier WATCHLIST | 1 | +103.5% | +103.5% to +103.5% | 1 | 1 | +103.5% | 0 |
| class RICH, legacy tier AVOID | 45 | +49.5% | -1.6% to +113.2% | 31 | 35 | +75.1% | 10 |
| latest print Q3 2019 (2020-01-03 to 2020-01-31) | 5 | +88.9% | +77.8% to +113.2% | 5 | 5 | +77.1% | 0 |
| latest print Q4 2019 (2020-02-05 to 2020-04-24) | 12 | +103.5% | +75.7% to +156.3% | 12 | 12 | +112.0% | 0 |
| latest print Q1 2020 (2020-04-30 to 2020-07-24) | 13 | +57.7% | +43.3% to +74.3% | 13 | 13 | +89.4% | 0 |
| latest print Q2 2020 (2020-07-31 to 2020-10-23) | 13 | +37.3% | +23.6% to +62.7% | 9 | 13 | +70.8% | 0 |
| latest print Q3 2020 (2020-10-30 to 2020-12-31) | 10 | +8.9% | -1.6% to +19.2% | 0 | 0 | +35.5% | 10 |

- **FAIR (the COVID fall) missed on the upside; RICH held only for the Q3 2020 print's entries.** The seven FAIR dates (2020-03-13 to
  2020-04-24, $1,072-1,283) returned +87.0% to +156.3% and beat SPY by 32.4 to 71.7 points; the three ACCUMULATE dates among them (March 20
  to April 3) were the series' best entries (+154.8% to +156.3%). The 46 RICH dates returned -1.6% to +113.2%; the ten that held are the
  Q3 2020 print's ($1,621-1,901, 2020-10-30 to 2020-12-31): -1.6% to +19.2%, short of the hurdle and 2.1 to 12.4 points behind SPY. Over three
  years +24.0% to +91.1% (median +64.2%); 48 beat SPY.
- **The price ranked the outcomes almost exactly** (-0.87 and -0.98; the EPP gap -0.83 and -0.98, Ratio B -0.77 and -0.96, the adjusted gap
  +0.56 and +0.83); the composite +0.23 and +0.31.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class RICH, legacy tier WATCHLIST | 13 | -3.4% | -9.6% to -0.9% | 0 | 1 | -23.3% | 12 |
| class RICH, legacy tier AVOID | 39 | -4.7% | -15.6% to +9.7% | 0 | 4 | -13.8% | 35 |
| latest print Q3 2020 (2021-01-08 to 2021-01-29) | 4 | +6.9% | -2.4% to +9.7% | 0 | 0 | +26.5% | 4 |
| latest print Q4 2020 (2021-02-04 to 2021-04-23) | 12 | -4.7% | -12.3% to +4.2% | 0 | 1 | +4.3% | 11 |
| latest print Q1 2021 (2021-04-29 to 2021-07-23) | 13 | -3.1% | -12.7% to +5.1% | 0 | 3 | -16.7% | 10 |
| latest print Q2 2021 (2021-07-29 to 2021-10-22) | 13 | -3.4% | -9.6% to -0.9% | 0 | 1 | -23.3% | 12 |
| latest print Q3 2021 (2021-10-28 to 2021-12-31) | 10 | -6.5% | -15.6% to -2.6% | 0 | 0 | -19.3% | 10 |

- **RICH held on 47 of 52: the 2021 entries ($1,736-2,999 as traded, before the 2022 twenty-for-one split) returned -15.6% to +9.7% over two
  years** and lagged SPY on 47 (by up to 19.6 points); 42 lost money. The five misses beat SPY by 0.1 to 2.9 points (March to May and
  2021-10-22). FY2021's print is outside the range; the anchor was FY20's $58.61 at 34.7-51.2x, the 89th-94th percentile. Over three years
  (to the end of 2024, with the first dividends in the late entries) the 2021 dates returned +6.0% to +68.7% (median +35.8%); 29 beat SPY and
  5 cleared the hurdle.
- **The m12-24 average ranked by the entry price** (-0.90; the EPP gap -0.91), the two-year return weakly (-0.33, -0.32); the adjusted gap
  +0.11 and -0.58, the composite -0.09 and -0.86.

## Across 2018-2021

- **RICH on 190 of 209 dates and right on 58:** the stock beat SPY over two years from 151 entries and cleared the hurdle from 107, and
  the RICH calls held only where the market caught up or the stock fell back: 2018-08-10, the Q3 2020 print's entries and most of 2021.
  The 19 FAIR dates all missed on the upside (median +113.9%, 53.7 points over SPY). Two-year returns ran from -15.6% to +156.3% (median
  +36.6%); 44 were losses, 42 of them 2021 entries.
- **The tier ordered the outcomes; the class barely did.** ACCUMULATE (3 dates) median +155.2%, WATCHLIST (44) +88.1%, AVOID (162) +30.1% over
  two years, and +69.2, +41.8 and +12.0 points over SPY. FAIR returned a median +113.9% and RICH +30.1%, but RICH spans a +145.1% entry
  (2019) and a -15.6% one (2021). Across the four years the EPP gap ranks best (-0.65 and -0.70), then the price (-0.59 and -0.37); Ratio B
  -0.41 and -0.35, the adjusted gap +0.10 and +0.06, the composite -0.35 and -0.47.
- Hypotheses only, to test on other tickers and periods and never to fold into GOOG's method or fact sheet: (1) a Tax Act year kept at GAAP
  by a narrow margin sets a deep BEAR (-35%/yr here) for a decade and an inflated XBULL two years later; the class barely depended on it, but
  the tier stayed AVOID through a doubling (2019-2020); (2) a RICH class that rests on the multiple against a window whose median sits near
  the post-2008 lows held only once the multiple itself was extreme (2021: 89th-94th percentile, 35-51x) and was wrong at 50th-90th; (3) the
  FAIR dates of a falling market (spring 2020) were the best entries, as the 2008-2009 batch's CHEAP floor dates were; (4) the composite's
  sign stayed unstable.

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class CHEAP, legacy tier BUY | 47 | +53.8% | +1.6% to +118.9% | 36 | 37 | +30.6% | 38 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +0.6% | +0.6% to +0.6% | 0 | 0 | -12.9% | 0 |
| class RICH, legacy tier AVOID | 4 | +13.7% | +0.3% to +15.4% | 0 | 2 | -7.5% | 2 |
| latest print Q3 2021 (2022-01-07 to 2022-01-28) | 4 | +13.7% | +0.3% to +15.4% | 0 | 2 | -7.5% | 2 |
| latest print Q4 2021 (2022-02-03 to 2022-04-22) | 12 | +8.7% | +0.6% to +32.0% | 0 | 2 | -3.3% | 2 |
| latest print Q1 2022 (2022-04-28 to 2022-07-22) | 13 | +58.7% | +45.5% to +69.4% | 13 | 13 | +24.1% | 13 |
| latest print Q2 2022 (2022-07-28 to 2022-10-21) | 13 | +52.1% | +33.8% to +74.3% | 13 | 12 | +40.9% | 13 |
| latest print Q3 2022 (2022-10-27 to 2022-12-30) | 10 | +90.9% | +72.0% to +118.9% | 10 | 10 | +74.1% | 10 |

- **CHEAP held on 38 of 48, RICH on 2 of 4.** The four January dates (RICH on FY20's anchor at 44-48x, $2,602-2,796 as traded) returned
  +0.3% to +15.4% over two years; the first two lagged SPY (held), the last two beat it by 0.6 and 2.2 points. The twelve CHEAP dates of the
  Q4 2021 print (2022-02-03 to 2022-04-22, $2,392-2,853 as traded, 21.3-25.4x FY21's $112.20) returned +0.6% to +32.0%: ten missed the
  hurdle and lagged SPY by 2.3 to 19.9 points. Every CHEAP entry from the Q1 2022 print on held (36 dates: $2,157-2,403 as traded and
  19.2-21.4x FY21's $112.20 to 2022-07-15, then $87-123 and 15.5-21.9x its $5.61 after the split): +33.8% to +118.9%, the Q3 2022 print's entries (October to
  December, the year's lows) +72.0% to +118.9%. SPY returned +3.2% to +67.2%. The two-year price landed nearest BASE on 46 dates and BEAR on
  5 (the first CHEAP entries). Over three years +10.0% to +256.1% (median +63.3%); 34 beat SPY.
- **Ranks:** the split-adjusted entry price -0.95 against the two-year return and -0.98 against the m12-24 average, the EPP gap -0.95 and
  -0.98, Ratio B -0.90 and -0.95, the adjusted gap +0.78 and +0.71, the composite -0.37 and -0.43.

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class CHEAP, legacy tier BUY | 9 | +99.0% | +80.0% to +125.2% | 9 | 9 | +81.3% | 9 |
| class CHEAP, legacy tier ACCUMULATE | 2 | +63.4% | +50.8% to +63.4% | 2 | 2 | +70.0% | 2 |
| class FAIR, legacy tier ACCUMULATE | 7 | +51.9% | +36.4% to +93.2% | 7 | 7 | +61.4% | 5 |
| class FAIR, legacy tier WATCHLIST | 4 | +48.6% | +36.0% to +59.7% | 4 | 3 | +44.3% | 3 |
| class RICH, legacy tier WATCHLIST | 11 | +45.4% | +35.8% to +118.9% | 11 | 7 | +40.1% | 0 |
| class RICH, legacy tier AVOID | 19 | +88.9% | +50.2% to +137.3% | 19 | 19 | +38.6% | 0 |
| latest print Q3 2022 (2023-01-06 to 2023-01-27) | 4 | +107.9% | +93.0% to +125.2% | 4 | 4 | +79.9% | 4 |
| latest print Q4 2022 (2023-02-03 to 2023-04-21) | 12 | +80.0% | +36.4% to +103.5% | 12 | 12 | +70.0% | 11 |
| latest print Q1 2023 (2023-04-27 to 2023-07-21) | 13 | +45.4% | +35.8% to +59.7% | 13 | 8 | +41.4% | 4 |
| latest print Q2 2023 (2023-07-27 to 2023-10-20) | 13 | +71.6% | +50.2% to +93.6% | 13 | 13 | +34.8% | 0 |
| latest print Q3 2023 (2023-10-26 to 2023-12-29) | 10 | +124.1% | +109.4% to +137.3% | 10 | 10 | +49.6% | 0 |

- **CHEAP held on all 11, FAIR on 8 of 11, RICH on none of 30.** The stock doubled from most entries: +35.8% to +137.3% over two years (SPY
  +26.9% to +67.6%), and every entry cleared the hurdle. The CHEAP dates ($88-104, 15.7-22.8x: four in January on FY21's $5.61, seven in February
  and March on FY22's $4.56) returned +50.8% to +125.2%. The 30 RICH dates (2023-05-19 to 2023-12-29, 26.9-31.3x FY22's $4.56, the
  64th-89th percentile of a window whose median was 25.6-25.9x) returned +35.8% to +137.3% and beat SPY on 26; the Q3 2023 print's entries (October to December) did best,
  +109.4% to +137.3%. The three FAIR misses beat SPY by 17 to 45 points. The two-year price landed nearest BULL on 41 dates and XBULL on 7.
  Over three years (46 dates) +104.2% to +264.1% (median +193.5%), all beating SPY.
- **Ranks:** the entry price +0.20 against the two-year return (the wrong sign) and -0.77 against the m12-24 average; the EPP gap +0.19 and
  -0.76, Ratio B +0.18 and -0.77, the adjusted gap -0.26 and +0.69, the composite -0.66 and -0.07.

## 2024 (52 dates; two-year horizons for the 46 to 2024-11-15)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class CHEAP, legacy tier ACCUMULATE | 1 | +119.9% | +119.9% to +119.9% | 1 | 1 | +72.6% | 1 |
| class FAIR, legacy tier ACCUMULATE | 5 | +116.9% | +113.2% to +138.2% | 5 | 5 | +60.8% | 0 |
| class FAIR, legacy tier WATCHLIST | 7 | +99.4% | +80.9% to +121.6% | 7 | 7 | +59.6% | 0 |
| class RICH, legacy tier WATCHLIST | 14 | +109.5% | +89.6% to +127.7% | 14 | 14 | +93.8% | 0 |
| class RICH, legacy tier AVOID | 19 | +104.8% | +58.8% to +134.1% | 19 | 19 | +58.3% | 0 |
| latest print Q3 2023 (2024-01-05 to 2024-01-26) | 4 | +131.7% | +117.8% to +132.0% | 4 | 4 | +49.5% | 0 |
| latest print Q4 2023 (2024-02-01 to 2024-04-19) | 12 | +116.9% | +80.9% to +138.2% | 12 | 12 | +59.7% | 1 |
| latest print Q1 2024 (2024-04-26 to 2024-07-19) | 13 | +104.8% | +83.4% to +134.1% | 13 | 13 | +58.3% | 0 |
| latest print Q2 2024 (2024-07-25 to 2024-10-25) | 14 | +109.5% | +89.6% to +121.6% | 14 | 14 | +96.1% | 0 |
| latest print Q3 2024 (2024-10-31 to 2024-11-15) | 3 | +62.1% | +58.8% to +69.2% | 3 | 3 | +91.3% | 0 |

- **RICH held on none of 33, FAIR on none of 12; the one CHEAP date held.** The 46 entries with a two-year horizon ($136-192, 23.5-33.7x
  FY22's $4.56 in January and FY23's $5.80 after) returned +58.8% to +138.2% (median +110.2%), all clearing the hurdle and beating SPY (+24.0% to +50.0%) by 26.6 to 93.8
  points: FY2024 came in at $8.03 and FY2025 at $10.80, against the $5.80 anchor. The GENAI watch list (from 2024-02-01) carried no
  information either way: those 42 dates returned a median +108.8%. The six dates of 2024-11-22 to 2024-12-27 have one-year results only
  (+60.4% to +88.2%). The two-year price landed nearest BULL on 37 dates and XBULL on 9.
- **Ranks:** the entry price -0.54 against the two-year return and -0.02 against the m12-24 average, the EPP gap -0.22 and -0.38, Ratio B
  -0.22 and -0.39, the adjusted gap +0.20 and +0.35, the composite +0.15 and -0.16.

## 2025 (52 dates; one-year horizons for the 46 to 2025-11-14, no two-year horizon yet)

| Group | Dates | Median 1-yr total return | Range | Cleared 15% hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class CHEAP, legacy tier BUY | 17 | +109.4% | +70.2% to +157.7% | 17 | 17 | n/a | - |
| class CHEAP, legacy tier ACCUMULATE | 6 | +88.2% | +64.2% to +97.7% | 6 | 6 | n/a | - |
| class FAIR, legacy tier ACCUMULATE | 4 | +75.3% | +64.8% to +88.2% | 4 | 4 | n/a | - |
| class FAIR, legacy tier WATCHLIST | 1 | +68.1% | +68.1% to +68.1% | 1 | 1 | n/a | - |
| class RICH, legacy tier WATCHLIST | 2 | +65.7% | +61.0% to +65.7% | 2 | 2 | n/a | - |
| class RICH, legacy tier AVOID | 16 | +39.3% | -1.0% to +70.8% | 13 | 13 | n/a | - |
| latest print Q3 2024 (2025-01-03 to 2025-01-31) | 5 | +65.1% | +63.1% to +70.8% | 5 | 5 | n/a | - |
| latest print Q4 2024 (2025-02-06 to 2025-04-17) | 11 | +80.2% | +64.2% to +121.9% | 11 | 11 | n/a | - |
| latest print Q1 2025 (2025-04-25 to 2025-07-18) | 13 | +109.6% | +86.6% to +157.7% | 13 | 13 | n/a | - |
| latest print Q2 2025 (2025-07-25 to 2025-10-24) | 14 | +46.8% | +22.1% to +88.2% | 14 | 14 | n/a | - |
| latest print Q3 2025 (2025-10-31 to 2025-11-14) | 3 | +1.8% | -1.0% to +5.9% | 0 | 0 | n/a | - |

- **One year only, so no call is scored.** The 46 entries returned -1.0% to +157.7% over one year (median +73.9%) against SPY's +10.7% to
  +36.3%, beating it on 43. The 23 CHEAP dates (2025-02-14 to 2025-07-18, $148-187, 18.4-23.3x FY24's $8.03) returned +64.2% to
  +157.7%; the 18 RICH dates (January on FY23's $5.80, late August to mid-November on FY24's $8.03, 25.7-35.4x) a median +39.3% for the 16
  of tier AVOID, the three latest (the Q3 2025 print's, 2025-10-31 to 2025-11-14) -1.0% to +5.9%, behind SPY.
- **Ranks against the one-year return:** the entry price -0.90, the EPP gap -0.79, Ratio B -0.85, the adjusted gap +0.76, the composite -0.07.

## 2026 (46 dates; six-month horizons for the 20 to 2026-05-15)

| Group | Dates | Median 6-month total return | Range | Cleared 7.2% hurdle | Beat SPY | Median m12-24 avg price | Call held |
| class FAIR, legacy tier ACCUMULATE | 1 | +24.8% | +24.8% to +24.8% | 1 | 1 | n/a | - |
| class FAIR, legacy tier WATCHLIST | 3 | +15.4% | +12.6% to +15.7% | 3 | 0 | n/a | - |
| class RICH, legacy tier WATCHLIST | 5 | +10.3% | +7.5% to +12.5% | 5 | 0 | n/a | - |
| class RICH, legacy tier AVOID | 11 | -1.3% | -28.4% to +13.1% | 3 | 1 | n/a | - |
| latest print Q3 2025 (2026-01-02 to 2026-01-30) | 5 | +7.2% | -2.9% to +13.1% | 2 | 1 | n/a | - |
| latest print Q4 2025 (2026-02-06 to 2026-04-24) | 12 | +11.4% | -7.2% to +24.8% | 10 | 1 | n/a | - |
| latest print Q1 2026 (2026-05-01 to 2026-05-15) | 3 | -27.3% | -28.4% to -25.5% | 0 | 0 | n/a | - |

- **Six months only, so no call is scored.** The 20 entries of January to mid-May (RICH 16, FAIR 4; 25.3-42.2x FY24's $8.03 in January and FY25's $10.80
  after) returned -28.4%
  to +24.8% over six months and lagged SPY on 18 (+0.2% to +22.2%); the Q1 2026 print's three entries (May, $383-397, 35.5-36.8x) fell 25.5% to 28.4% by
  November. The 26 later dates have no horizon yet.

## Across 2022-2026

- **150 two-year horizons (2022-01-07 to 2024-11-15): no loss, median +80.8%;** 134 cleared the hurdle and 132 beat SPY. The call held on
  60: CHEAP 50 of 60 (median +63.4%, 14.8 points over SPY), FAIR 8 of 23 (+92.3%) and RICH 2 of 67 (+98.0%, 55.8 points over SPY). The
  class ordered the outcomes backwards: the stock's multiple against its own 2012-2022 window (median about 25x) read RICH from mid-2023 while
  EPS rose from $4.56 (FY22) to $10.80 (FY25).
- **The tier did not order them either:** BUY (56) median +63.8%, ACCUMULATE (16) +63.4%, WATCHLIST (36) +99.4%, AVOID (42) +93.9%. Across
  the 150, the split-adjusted entry price ranks +0.57 against the two-year return (the higher the entry, the better the outcome, because the
  higher prices came later and were followed by the 2024-2026 earnings run), the EPP gap +0.23, Ratio B +0.25, the adjusted gap -0.37 and the
  composite -0.44: every measure has the wrong sign. Within a single year the price and the EPP gap ranked well in 2022 and in the 2025
  one-year results (-0.90 to -0.98), not in 2023-2024.
- Hypotheses only, to test on other tickers and periods and never to fold into GOOG's method or fact sheet: (1) a P/E of the last full
  year's EPS against the stock's own window misreads a company whose earnings then compound at a third a year (FY22 to FY25 EPS +33%/yr):
  the trailing multiple looks rich while the later one is ordinary; (2) the floor and the price ranked the outcomes well within 2022 and in the 2025 one-year
  results, and not in 2023-2024, as in 2018-2021 they did in some years only; (3) a company-acknowledged disruption theme on the watch list, with no market read, said nothing about
  the outcome (GENAI dates: median +108.8% over two years); (4) FY2017 at GAAP, still setting BEAR (-35.4%/yr) and XBULL (+65.3%/yr) on every
  date, kept the tier from separating anything, and the composite's sign stayed unstable.
