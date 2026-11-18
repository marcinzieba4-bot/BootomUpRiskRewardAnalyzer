# GOOG retrospective findings (hindsight)

Patterns seen in `outcome.json` for the GOOG weekly dates: 105, from 2008-01-04 to 2009-12-31, all Google Inc. (the Class A common
stock, NASDAQ: GOOG). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored
only after its point-in-time build was committed and pushed (f268b6d, firewall result 4d0926c); the outcomes were computed on
2026-11-18. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31). Google paid no dividend, so total
returns are price returns, and the 2014 share distribution falls after every horizon, so prices are as traded. Medians of an even count
take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY); FAIR should land within 15 points of the benchmark; RICH
should miss the hurdle and lag the benchmark.

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
