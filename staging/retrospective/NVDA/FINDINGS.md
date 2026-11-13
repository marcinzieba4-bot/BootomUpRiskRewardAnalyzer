# NVDA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NVDA weekly dates: 731 from 2008-01-04 to 2021-12-31, all NVIDIA Corporation (Nasdaq: NVDA).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 9510254, firewall result 99a5d02; 2010-2013: 69a20a9, firewall result
858dc95; 2014-2017: 3464af5, firewall result c0c01f1; 2018-2021: 0b46410, firewall result 6520554); the outcomes were computed on
2026-11-12 (2008-2009) and 2026-11-13 (2010-2013, 2014-2017, 2018-2021). Every date has its 6-month, 1-, 2- and 3-year horizons (the
last ends 2024-12-31). Prices are on the AS_OF share basis: no split falls in a horizon of the 2008-2017 dates, so their prices are as
traded; the four-for-one split of 2021-07-20 falls in horizons of the 2018-2021 dates and the ten-for-one of 2024-06-10 in the
three-year horizons of the dates from 2021-06-11, and prices after a split are restated to the AS_OF basis (2018 to mid-2021 dates read
the 2022 low of $112.27 as $449.08). NVIDIA paid no dividend until November 2012: its first ($0.075 a share on this basis, ex-date 2012-11-20)
falls only inside the three-year horizon of the dates from 2009-11-20 on, and the total returns of later dates include the dividends
paid inside their horizons. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is
+32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark
(SPY), FAIR should land within ±15pp of the benchmark, and RICH should miss the hurdle and lag the benchmark.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -13.1% | -49.7% to +115.5% | 13 | 20 | +5.6% | 20 |
| FY08E $0.767 (2008-01-04 to 2008-02-08) | 6 | -32.9% | -38.4% to -31.1% | 0 | 0 | -50.6% | 0 |
| FY09E $1.31 (2008-02-15 to 2008-12-31) | 47 | -11.3% | -49.7% to +115.5% | 13 | 20 | +17.7% | 20 |
| latest print Q3 FY08 (2008-01-04 to 2008-02-08) | 6 | -32.9% | -38.4% to -31.1% | 0 | 0 | -50.6% | 0 |
| latest print Q4 FY08 (2008-02-15 to 2008-05-02) | 12 | -11.9% | -30.2% to -5.8% | 0 | 4 | -29.1% | 4 |
| latest print Q1 FY09 (2008-05-09 to 2008-08-08) | 14 | -37.8% | -49.7% to -10.4% | 0 | 0 | -23.6% | 0 |
| latest print Q2 FY09 (2008-08-14 to 2008-10-31) | 12 | +4.9% | -27.8% to +78.5% | 4 | 7 | +38.3% | 7 |
| latest print Q3 FY09 (2008-11-07 to 2008-12-31) | 9 | +84.9% | +44.6% to +115.5% | 9 | 9 | +81.2% | 9 |

- **CHEAP held on 20 of 53 dates, and the misses came first.** The 26 entries from 2008-01-04 to 2008-06-27 ($18.32-30.00, 14.0-39.1x
  the last full year's EPS) returned -49.7% to -5.8% over two years; four of March-April 2008 beat SPY by 0.1-2.2pp, so their calls held,
  and the other 22 lagged it by 1.5-31.6pp. The 13 from 2008-07-03 (the day after the warranty charge 8-K) to 2008-09-26 ($10.19-13.61,
  7.8-10.4x) returned -27.8% to +4.9% and held twice (2008-09-12 and 2008-09-26, by beating a falling SPY). The 14 from 2008-10-03 to the
  end of the year ($6.38-9.03, 4.9-6.9x) returned +25.7% to +115.5%, all beat SPY, and 13 cleared the hurdle. Every 2008 date sat through
  a 53-80% drawdown, 46 of them to the 2008-11-20 close of $5.90; the two-year high was $18.88 (2010-01-06) for the 28 dates from
  2008-06-27 on.
  Over three years (to the end of 2011) the 2008 dates returned -47.4% to +129.3% (median +4.7%); 28 beat SPY and 13 cleared the
  three-year hurdle.
- **The anchor was the peak year.** From the Q4 FY08 print every model carried FY08's $1.31 (the last full year, no EPS guide in any
  filing). FY2009 came in at a $(0.05) loss and FY2010 at $(0.12) (the Q4 FY10 release, 2010-02-17, outside the series), so the
  "4.9-10.4x" of the second half of 2008 was a multiple of earnings that did not recur within the horizon. The EPP floor (15-16x FY08,
  $19.65-20.96, and $16.10 on FY07's EPS in January) was reached within two years only by the 25 entries to 2008-06-20, through the
  highs of the first half of 2008 ($20.10-28.89) that preceded the fall; from 2008-06-27 no two-year high came back to it. Hypothesis, not a rule: for a company that files its own business as
  cyclical, the last full year at a cyclical high overstates the EPS a floor and a P/E percentile can lean on; test it on other
  CYCLICAL tickers and periods (XOM, BKR and CAT in 2008), never fit it to NVDA.
- **The window's multiples were the IPO's and the dot-com's.** January 2008's 32-39x sat at the 44th-54th percentile of a 9.0-year
  window (median 36.4-36.7x) whose calendar-year lows were 13-34x, so a stock at 14-19x after the Q4 FY08 print read as the 1st-21st
  percentile of its own history. The scenarios came from the same decade: BULL +66%/yr and XBULL +294%/yr from the FY1999-FY2001 run,
  BEAR -64%/yr from the restated FY2003 fall. No two-year price came near BULL (the highest was 0.17x the BULL price).
- **The ranks run through the price, and the composite had the wrong sign.** Across the 53 dates the entry price ranks the two-year
  return at Spearman -0.89 and the return to the m12-24 average price at -0.99; the EPP gap and Ratio B rank them the same way (within
  one EPS anchor both move with the price), the right signs. The adjusted gap ranks them at -0.42 and -0.50 and the proxy composite at
  -0.64 and -0.86, the wrong signs: the composite was 2.85-2.50 on the entries of January to early August 2008 (revenue +36%, margins
  rising, inventories falling against revenue), which returned the least, and 1.35 on those of November-December, which returned the most.
- **The two-year price landed nearest BEAR on 44 dates and BASE on 9** (the nine from the Q3 FY09 print, when BASE was -26.1%/yr and the
  BASE price $20.81-21.31). Every landing sat between the BEAR price ($2.60-2.86) and the BASE price, at 0.14-0.72 times BASE.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +41.4% | -25.8% to +236.8% | 27 | 23 | +30.8% | 29 |
| FY09E $1.31 (2009-01-09 to 2009-02-06) | 5 | +188.2% | +150.6% to +198.9% | 5 | 5 | +70.8% | 5 |
| FY10E $1.31 (2009-02-12 to 2009-12-31) | 47 | +18.9% | -25.8% to +236.8% | 22 | 18 | +27.9% | 24 |
| latest print Q3 FY09 (2009-01-09 to 2009-02-06) | 5 | +188.2% | +150.6% to +198.9% | 5 | 5 | +70.8% | 5 |
| latest print Q4 FY09 (2009-02-12 to 2009-05-01) | 12 | +84.2% | +45.8% to +236.8% | 12 | 10 | +48.5% | 12 |
| latest print Q1 FY10 (2009-05-08 to 2009-07-31) | 13 | +48.7% | +7.0% to +108.9% | 10 | 6 | +40.5% | 10 |
| latest print Q2 FY10 (2009-08-07 to 2009-10-30) | 13 | -4.9% | -15.8% to +30.4% | 0 | 2 | +17.0% | 2 |
| latest print Q3 FY10 (2009-11-06 to 2009-12-31) | 9 | +8.0% | -25.8% to +12.6% | 0 | 0 | +18.7% | 0 |

- **CHEAP held on 29 of 52 dates: the first half of the year.** The 27 entries from 2009-01-09 to 2009-07-10 ($7.61-12.04, 5.8-9.2x)
  returned +36.0% to +236.8% over two years and all cleared the hurdle; 21 of them also beat SPY, whose own two-year return from those
  dates was +38.9% to +98.7%. The 25 from 2009-07-17 to the end of the year ($11.96-18.68, 9.1-14.3x) returned -25.8% to +30.4%; two
  (2009-10-16 and 2009-10-30) beat SPY by about 2pp, and the other 23 lagged it by 0.7-42.8pp and missed the hurdle. The two-year high was
  $25.68 (2011-02-17) for 46 dates and the low $8.88 (2010-08-11) for 34; every 2009 date sat through a 53-54% drawdown. Over three years
  (to the end of 2012) the 2009 dates returned -34.8% to +108.3% (median +10.0%); 6 beat SPY and 9 cleared the three-year hurdle.
- **The floor was reached by every 2009 entry, and not held.** Each model put the price 11-61% under a 14-17x floor ($18.34-22.27, on
  FY08's $1.31); every date's two-year high reached it (the highs of January-February 2011, $19.87-25.68), but the two-year price was
  back under it on 42 of the 52 dates (all but the ten from 2009-01-09 to 2009-03-06 and 2009-05-01). The earnings the anchor assumed
  did not come within the horizon: FY2010 lost $(0.12) a share (the Q4 FY10 release).
- **The ranks run through the price again.** The entry price ranks the two-year return at Spearman -0.96 and the m12-24 average at -0.97;
  the EPP gap at -0.92 and -0.99 and Ratio B at -0.73 and -0.76 (the right signs); the adjusted gap at -0.73 and -0.59 and the proxy
  composite at -0.70 and -0.58 (the wrong signs): the composite was 1.15-1.35 from the Q4 FY09 print to July (every signal at BEAR on Q4
  FY09) and 2.30-2.65 from the Q2 FY10 print, while the returns fell from the first group to the second.
- **The two-year price landed nearest BASE on 30 dates and BEAR on 22.** BASE was below the entry price from 2009-02-12 to 2009-05-01
  ($5.10-5.74, the Q4 FY09 quarter's -60% carried forward) and $12.76 from the Q1 FY10 print (it was $20.66-20.74 in January 2009); the
  stock ended those 30 two-year horizons at $13.83-25.67, 0.96-5.03 times BASE. From 2009-08-07 BASE was $33.18, then $146-149 on the
  Q4 FY10 guide (+91.5% on the trough quarter); the two-year prices of $11.73-15.72 landed nearest BEAR. The Q4 FY10 quarter itself came in at $982.5M, above the guided $921.3M.

## Across 2008-2009

- **One price state for two years; the outcome followed the entry point.** CHEAP and BUY on all 105 dates, robust 8 of 8 on every one,
  while the two-year return ran from -49.7% to +236.8%. What separated the calls that held (49 of 105) from those that missed was the
  timing against the low: the 41 entries from 2008-10-03 to 2009-07-10 ($6.38-12.04) all held, while 8 of the 64 before and after did,
  including only two of the 13 at $10.19-13.61 in July-September 2008. Hypotheses only: a CHEAP class for a self-described cyclical at its peak earnings is a statement about the multiple, not the earnings; and the
  signal composite, built from year-on-year quarter changes, read best at the top and worst at the bottom of this cycle. Test both on other
  tickers and periods; never fold them into NVDA's method or fact sheet.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | -3.1% | -21.6% to +57.7% | 6 | 6 | +9.9% | 6 |
| FY10E $1.31 (2010-01-08 to 2010-02-12) | 6 | -8.4% | -21.6% to -2.5% | 0 | 0 | -0.4% | 0 |
| FY11E $1.31 (2010-02-19 to 2010-12-31) | 46 | +0.2% | -20.9% to +57.7% | 6 | 6 | +14.5% | 6 |
| latest print Q3 FY10 (2010-01-08 to 2010-02-12) | 6 | -8.4% | -21.6% to -2.5% | 0 | 0 | -0.4% | 0 |
| latest print Q4 FY10 (2010-02-19 to 2010-05-07) | 12 | -15.0% | -19.5% to -2.5% | 0 | 0 | -9.1% | 0 |
| latest print Q1 FY11 (2010-05-14 to 2010-08-06) | 13 | +13.6% | -5.6% to +46.7% | 2 | 2 | +27.6% | 2 |
| latest print Q2 FY11 (2010-08-13 to 2010-11-05) | 13 | +21.3% | +0.2% to +57.7% | 4 | 4 | +29.2% | 4 |
| latest print Q3 FY11 (2010-11-12 to 2010-12-31) | 8 | -14.9% | -20.9% to -10.1% | 0 | 0 | -5.6% | 0 |

- **CHEAP held on 6 of 52 dates, the six at the year's low.** The entries of 2010-07-30 to 2010-09-03 ($9.19-10.12, 7.0-7.7x FY08's
  $1.31) returned +41.7% to +57.7% over two years and beat SPY by 4.5-23.0pp. The 18 entries to 2010-05-07 ($13.96-18.55) returned
  -21.6% to -2.5% and lagged SPY by 30.4-40.9pp; the other 20 of 2010-05-14 to 2010-11-05 ($10.05-13.14) returned -5.6% to +31.9%,
  just short of the hurdle at best, and lagged SPY by 1.5-31.0pp; the 8 from the Q3 FY11 print ($13.26-15.40) returned -20.9% to
  -10.1%. Every 2010 date sat through a 54-56% drawdown. Over three years (to the end of 2013) the 2010 dates returned -32.3% to +59.2%
  (median +17.8%); none beat SPY (+33.9% to +66.1%) and 7 cleared the three-year hurdle.
- **The floor was reached by every entry and held by none.** Each model put the price 6-61% under a 15-18x floor on FY08's $1.31
  ($19.65-23.58); every date's two-year high was the $25.68 of 2011-02-17, above it, and every date ended its two years 19-50% under
  it ($11.70-15.90). FY08's $1.31 did not come back within the horizon: FY2011 earned $0.43 (Q4 FY11 release, 2011-02-16) and FY2012
  $0.94 (Q4 FY12 release, 2012-02-15).
- **The two-year price landed nearest BEAR on all 52 dates,** because BASE was far above it: the guides of Q4 FY10 to Q4 FY11 put
  BASE at +88.9% to -12.2%/yr on FY08's $1.31 and the BASE price at $29-145, while the BEAR price was $2.09-2.89; the two-year prices
  were 0.09-0.43 times BASE.
- **The ranks run through the price.** The entry price ranks the two-year return at Spearman -0.88 and the m12-24 average at -0.95; the
  EPP gap at -0.86 and -0.91 and Ratio B at -0.66 and -0.70 (the right signs); the adjusted gap and the proxy composite at -0.27 and -0.34
  (the wrong signs): the composite was 3.50 and 3.20 on the Q4 FY10 and Q1 FY11 prints (to 2010-08-06) and 2.00 from the Q2 FY11 print,
  which held four of the six calls that held.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 14 | +13.3% | -52.3% to +29.4% | 0 | 0 | -3.1% | 0 |
| class RICH, legacy tier AVOID | 12 | -31.0% | -50.0% to -27.6% | 0 | 0 | -30.9% | 12 |
| class RICH, legacy tier WATCHLIST | 4 | -20.5% | -24.3% to -17.1% | 0 | 0 | -29.7% | 4 |
| class RICH, legacy tier ACCUMULATE | 1 | -14.3% | -14.3% to -14.3% | 0 | 0 | -24.0% | 1 |
| class CHEAP, legacy tier ACCUMULATE | 19 | +5.2% | -11.3% to +18.0% | 0 | 0 | -7.7% | 0 |
| class CHEAP, legacy tier WATCHLIST | 2 | +4.7% | +2.6% to +4.7% | 0 | 0 | -6.0% | 0 |
| FY11E $1.31 (2011-01-07 to 2011-02-11) | 6 | -46.4% | -52.3% to -35.4% | 0 | 0 | -43.0% | 0 |
| FY12E $0.43 (2011-02-18 to 2011-12-30) | 46 | +0.4% | -50.0% to +29.4% | 0 | 0 | -12.6% | 17 |
| latest print Q3 FY11 (2011-01-07 to 2011-02-11) | 6 | -46.4% | -52.3% to -35.4% | 0 | 0 | -43.0% | 0 |
| latest print Q4 FY11 (2011-02-18 to 2011-05-06) | 12 | -31.0% | -50.0% to -27.6% | 0 | 0 | -30.9% | 12 |
| latest print Q1 FY12 (2011-05-13 to 2011-08-05) | 13 | -8.9% | -24.3% to +16.3% | 0 | 0 | -17.5% | 5 |
| latest print Q2 FY12 (2011-08-12 to 2011-11-04) | 13 | +12.3% | -0.6% to +29.4% | 0 | 0 | -4.4% | 0 |
| latest print Q3 FY12 (2011-11-11 to 2011-12-30) | 8 | +14.1% | +2.6% to +18.0% | 0 | 0 | -0.9% | 0 |

- **RICH held on all 17 dates; CHEAP on none of 35.** The RICH entries of 2011-02-18 to 2011-06-10 ($17.12-25.63, 39.8-59.6x FY11's
  $0.43) returned -50.0% to -14.3% over two years and lagged SPY by 46.4-67.3pp; the stock stood at $12.30-14.84 two years later.
  The six CHEAP entries of January-February 2011 ($19.87-25.67, on FY08's $1.31) returned -52.3% to -35.4% ($12.16-12.77 two years
  later). The 29 CHEAP entries from 2011-06-17 ($11.73-16.15, 27.3-37.6x FY11's $0.43, CHEAP on Ratio B with the guides' BASE of
  +18.7% to +24.9%/yr) returned -11.3% to +29.4%: none cleared the hurdle, and all lagged SPY (+25.0% to +60.6%) by 22.3-47.4pp. All
  52 dates had their two-year low at the $11.38 of 2012-11-16 (drawdowns of 31-56%). Over three years (to the end of 2014) the 2011
  dates returned -37.8% to +70.6% (median +23.8%); none beat SPY and 5 cleared the three-year hurdle.
- **The RICH call rested on a depressed year, and held although the earnings came back.** FY11's $0.43 carried the Q2 FY11 warranty
  charge and inventory write-down; FY2012 earned $0.94 (Q4 FY12 release, 2012-02-15), more than twice it, yet the price fell, because
  the multiple fell further: from 40-60x FY11's $0.43 to 13-17x FY12's $0.94 a year later. The RICH class held on the multiple, not on
  the earnings. It depends on a judgement call: with FY2011 excluded as a distorted year (a point-in-time variant, run before these
  outcomes), FY08's $1.31 would have carried 2011 and all 17 RICH dates would have read CHEAP, and missed. The README records the call and
  the test behind it; the outcome must not be read as support for it.
- **The ranks run through the price, and this year the composite had the right sign.** The entry price ranks the two-year return at
  Spearman -0.97 and the m12-24 average at -0.99; the adjusted gap at +0.81 and +0.81 and the proxy composite at +0.84 and +0.79 (the
  right signs): the composite was 2.30 on the Q4 FY11 print (the RICH dates of February-May, the worst returns) and 3.00 on the Q2 FY12
  print (August-November). The EPP gap (-0.39, -0.43) and Ratio B (-0.33, -0.35) rank them more weakly, as the anchor changed from
  $1.31 to $0.43 in February.
- **The two-year price landed nearest BASE on 46 dates and BEAR on 6** (the January-February entries on FY08's $1.31, whose BASE price
  was $28.68-28.99). From the Q4 FY11 print the BASE price was $11.88-21.51; the two-year prices of $12.30-15.97 sat near it.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 3 | +14.7% | +11.9% to +15.2% | 0 | 0 | +1.0% | 0 |
| class CHEAP, legacy tier WATCHLIST | 1 | +6.3% | +6.3% to +6.3% | 0 | 0 | -3.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 2 | +2.5% | +0.3% to +2.5% | 0 | 0 | -8.4% | 0 |
| class CHEAP, legacy tier BUY | 46 | +44.8% | +15.4% to +81.6% | 37 | 26 | +29.2% | 37 |
| FY12E $0.43 (2012-01-06 to 2012-02-10) | 6 | +11.9% | +0.3% to +15.2% | 0 | 0 | -2.2% | 0 |
| FY13E $0.94 (2012-02-17 to 2012-12-28) | 46 | +44.8% | +15.4% to +81.6% | 37 | 26 | +29.2% | 37 |
| latest print Q3 FY12 (2012-01-06 to 2012-02-10) | 6 | +11.9% | +0.3% to +15.2% | 0 | 0 | -2.2% | 0 |
| latest print Q4 FY12 (2012-02-17 to 2012-05-04) | 12 | +27.3% | +15.4% to +54.2% | 3 | 3 | +4.4% | 3 |
| latest print Q1 FY13 (2012-05-11 to 2012-08-03) | 13 | +49.9% | +33.0% to +63.5% | 13 | 6 | +29.6% | 13 |
| latest print Q2 FY13 (2012-08-10 to 2012-11-02) | 13 | +43.2% | +33.8% to +61.6% | 13 | 9 | +29.2% | 13 |
| latest print Q3 FY13 (2012-11-09 to 2012-12-28) | 8 | +77.3% | +61.1% to +81.6% | 8 | 8 | +51.7% | 8 |

- **CHEAP held on 37 of 50 dates, every one from 2012-04-20.** From the Q4 FY12 print (FY13E $0.94) the 46 entries ($11.38-15.85,
  12.1-16.9x) returned +15.4% to +81.6% (median +44.8%). The nine of 2012-02-17 to 2012-04-13 ($14.16-15.85, 15.1-16.9x) returned
  +15.4% to +31.3%, short of the hurdle, and lagged SPY by 5.9-24.2pp; the 37 from 2012-04-20 all cleared it, and 26 of them also beat
  SPY (+35.8% to +55.5%). The four CHEAP and two FAIR entries of January-February 2012 (on FY11's $0.43) returned +0.3% to +15.2%: the
  CHEAP calls missed, and the FAIR ones (+0.3% and +2.5%) lagged SPY by 33.9 and 36.2pp, outside the ±15pp a FAIR call allows. The
  two-year low was the $11.38 of 2012-11-16 for 45 dates (drawdowns of 14-31%); the stock stood at $16.85-21.07 two years later, over the
  16x floor ($15.04) on every date. Over three years (to the end of 2015) the 2012 dates returned +31.7% to +185.6% (median +69.8%); 34
  beat SPY and 40 cleared the three-year hurdle.
- **The anchor was close to the next year.** FY12's $0.94 stood for FY13E; FY2013 earned $0.90 (Q4 FY13 release, 2013-02-13). The
  calls at 12-17x held on the multiple: by the end of their two years the stock traded at 19-23x FY13's $0.90.
- **Every rank but the composite's has the right sign.** The entry price ranks the two-year return at Spearman -0.92 and the m12-24
  average at -0.94, the EPP gap at -0.95 and -0.94, Ratio B at -0.89 and -0.84, the adjusted gap at +0.65 and +0.68; the proxy composite
  at -0.51 and -0.51 (the wrong sign): it was 2.35-2.50 on the entries of January to early May, which returned least, and 2.00-2.30
  from the Q1 FY13 print on.
- **The two-year price landed nearest BASE on 38 dates and BEAR on 14** (between 2012-08-10 and 2012-12-14, where the Q3 and Q4 FY13
  guides put the BASE price at $28-29, about as far above the two-year price as the $11 BEAR price was below it). The two-year prices
  were 0.60-0.88 times BASE.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +69.2% | +39.6% to +122.9% | 53 | 53 | +43.0% | 53 |
| FY13E $0.94 (2013-01-04 to 2013-02-08) | 6 | +69.4% | +58.0% to +72.1% | 6 | 6 | +52.7% | 6 |
| FY14E $0.9 (2013-02-15 to 2013-12-31) | 47 | +69.2% | +39.6% to +122.9% | 47 | 47 | +42.7% | 47 |
| latest print Q3 FY13 (2013-01-04 to 2013-02-08) | 6 | +69.4% | +58.0% to +72.1% | 6 | 6 | +52.7% | 6 |
| latest print Q4 FY13 (2013-02-15 to 2013-05-03) | 12 | +80.4% | +68.8% to +93.3% | 12 | 12 | +52.3% | 12 |
| latest print Q1 FY14 (2013-05-10 to 2013-08-02) | 13 | +48.2% | +39.6% to +58.8% | 13 | 13 | +39.5% | 13 |
| latest print Q2 FY14 (2013-08-09 to 2013-11-01) | 13 | +59.5% | +47.8% to +92.2% | 13 | 13 | +38.0% | 13 |
| latest print Q3 FY14 (2013-11-08 to 2013-12-31) | 9 | +111.6% | +88.7% to +122.9% | 9 | 9 | +47.7% | 9 |

- **CHEAP held on all 53 dates.** The entries ($12.17-16.17, 12.9-18.0x) returned +39.6% to +122.9% over two years (median +69.2%),
  cleared the hurdle and beat SPY (+14.6% to +45.3%) by 11.2-103.5pp; the stock stood at $19.20-33.75 two years later, and the drawdowns
  were 16-18%. The nine entries from the Q3 FY14 print returned +88.7% to +122.9%: their horizons end in November-December 2015, after
  the stock's rise of October-December 2015. Over three years (to the end of 2016) the 2013 dates returned +110.3% to +652.2% (median +240.4%); all
  beat SPY and cleared the three-year hurdle.
- **The return came from the multiple, not the anchor.** FY13's $0.90 stood for FY14E; FY2014 earned $0.74 (Q4 FY14 release,
  2014-02-12, outside the series), less, and the stock still rose.
- **Within the year the price ranks nothing.** The entry price ranks the two-year return at Spearman +0.11 (the m12-24 average at
  -0.67); the EPP gap at +0.12 and -0.66, Ratio B at +0.13 and -0.63, the adjusted gap at -0.23 and +0.51, the proxy composite at -0.29
  and +0.32. The entries spanned $12.17-16.17, and the end of each two-year window, before or after the rise of late 2015, decided the
  ordering.
- **The two-year price landed nearest BASE on 40 dates, BULL on 12** (2013-10-18 to 2013-12-31) **and BEAR on 1** (2013-02-01).

## Across 2010-2013

- **The class followed the anchor, and the anchor followed the cycle.** CHEAP held on 96 of 190 dates, RICH on 17 of 17, FAIR on none
  of 2: 113 of 209 (162 of 314 with 2008-2009). Each year's anchor was the last full GAAP year: in 2010 the cyclical high of FY2008
  ($1.31), not earned again within the horizon, so 7-14x read CHEAP and held only at the low of mid-2010; in 2011 the depressed FY2011
  ($0.43), so 40-60x read RICH and held, although FY2012 earned twice as much; in 2012-2013 FY2012 and FY2013 ($0.94, $0.90), close to
  the year that followed, and the CHEAP calls at 12-18x held from April 2012 on. Hypotheses only: for a company that files its own
  business as cyclical, a P/E on the last full year reads the cycle's phase as much as the price (peak year: CHEAP; trough year:
  RICH), and the calls held best when the anchor sat near mid-cycle. Test them on other CYCLICAL tickers and periods; never fold them
  into NVDA's method or fact sheet.
- **The composite has no stable sign.** The proxy composite ranks the two-year return with the right sign in 2011 (+0.84) and the wrong
  one in 2008, 2009, 2010, 2012 and 2013 (-0.27 to -0.70); within one anchor the entry price ranked the outcome in 2010-2012 (-0.88 to
  -0.97), and in 2013, when the price barely moved, nothing did.
- **The judgement calls touch the right dates.** The 17 RICH calls that held depend on FY2011 kept at GAAP (19 classes move if it is
  excluded); the CHEAP calls of 2010 depend on FY2010 excluded rather than kept at its non-GAAP $0.26 (49 of the 63 classes the
  non-GAAP variant moves in 2010-2012 are 2010's). Both were decided by the frozen rules before any 2010-2013 outcome was computed, and
  the variants were run before it too; they are the calls a reader with hindsight should check first.

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 5 | +87.6% | +71.2% to +93.0% | 5 | 5 | +55.0% | 5 |
| class FAIR, legacy tier ACCUMULATE | 6 | +80.3% | +47.8% to +303.1% | 6 | 6 | +37.8% | 0 |
| class FAIR, legacy tier WATCHLIST | 30 | +155.4% | +87.0% to +287.1% | 30 | 30 | +66.0% | 0 |
| class RICH, legacy tier AVOID | 10 | +353.0% | +217.3% to +437.5% | 10 | 10 | +130.1% | 0 |
| FY14E $0.90 (2014-01-10 to 2014-02-07) | 5 | +87.6% | +71.2% to +93.0% | 5 | 5 | +55.0% | 5 |
| FY15E $0.74 (2014-02-14 to 2014-12-26) | 46 | +213.3% | +47.8% to +437.5% | 46 | 46 | +81.1% | 0 |
| latest print Q3 FY14 (2014-01-10 to 2014-02-07) | 5 | +87.6% | +71.2% to +93.0% | 5 | 5 | +55.0% | 5 |
| latest print Q4 FY14 (2014-02-14 to 2014-05-02) | 12 | +98.7% | +47.8% to +104.2% | 12 | 12 | +43.2% | 0 |
| latest print Q1 FY15 (2014-05-07 to 2014-08-01) | 13 | +150.5% | +97.6% to +225.2% | 13 | 13 | +59.0% | 0 |
| latest print Q2 FY15 (2014-08-08 to 2014-10-31) | 13 | +238.0% | +213.3% to +303.1% | 13 | 13 | +104.0% | 0 |
| latest print Q3 FY15 (2014-11-07 to 2014-12-26) | 8 | +358.3% | +264.3% to +437.5% | 8 | 8 | +132.0% | 0 |

- **CHEAP held on all 5 dates, FAIR on none of 36, RICH on none of 10.** The five CHEAP entries of January-February 2014 (FY13's $0.90,
  $15.56-15.99, 17.3-17.8x) returned +71.2% to +93.0% over two years and beat SPY by 62.1-84.5pp. Every later entry (FY14's $0.74 for
  FY15E, $16.85-21.07, 22.8-28.5x) returned more: the 36 FAIR ones +47.8% to +303.1%, beating SPY by 42.0-285.2pp, so none landed within
  the ±15pp a FAIR call allows, and the 10 RICH ones (2014-09-05 and 2014-10-31 to 2014-12-26) +217.3% to +437.5%. The later the entry,
  the further its window reached into the rise that began in October 2015: the two-year prices run from $25.73 to $109.78. The two-year
  lows were the $16.79 of 2014-10-13 for 35 dates (drawdowns of 18-25%). Over three years every 2014 date returned +441.5% to
  +1,043.1%.
- **The anchor was low, then far too low.** FY14's $0.74 stood for FY15E; FY2015 earned $1.12, FY2016 $1.08 and FY2017 $2.57.
- **Every rank had the wrong sign.** The entry price ranks the two-year return at Spearman +0.62 (the m12-24 average at +0.46), the EPP
  gap at +0.62 and +0.46, Ratio B at +0.77 and +0.63, the proxy composite at +0.80 and +0.70; the adjusted gap at -0.25 and -0.03. The
  dearer entries came later and caught more of the rise.
- **The two-year price landed nearest BULL on 36 dates, XBULL on 13 and BASE on 2.**

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 3 | +728.9% | +683.2% to +760.6% | 3 | 3 | +411.6% | 3 |
| class FAIR, legacy tier BUY | 3 | +383.9% | +377.5% to +389.7% | 3 | 3 | +187.6% | 0 |
| class FAIR, legacy tier ACCUMULATE | 8 | +612.7% | +337.3% to +723.3% | 8 | 8 | +316.8% | 0 |
| class FAIR, legacy tier WATCHLIST | 13 | +535.0% | +333.7% to +688.4% | 13 | 13 | +278.6% | 0 |
| class RICH, legacy tier WATCHLIST | 4 | +654.3% | +477.6% to +709.7% | 4 | 4 | +386.7% | 0 |
| class RICH, legacy tier AVOID | 22 | +567.7% | +370.3% to +628.6% | 22 | 22 | +348.8% | 0 |
| FY15E $0.74 (2015-01-02 to 2015-02-06) | 6 | +442.4% | +411.7% to +479.4% | 6 | 6 | +183.1% | 0 |
| FY16E $1.12 (2015-02-13 to 2015-12-31) | 47 | +584.9% | +333.7% to +760.6% | 47 | 47 | +346.1% | 3 |
| latest print Q3 FY15 (2015-01-02 to 2015-02-06) | 6 | +442.4% | +411.7% to +479.4% | 6 | 6 | +183.1% | 0 |
| latest print Q4 FY15 (2015-02-13 to 2015-05-01) | 12 | +372.9% | +333.7% to +421.7% | 12 | 12 | +224.4% | 0 |
| latest print Q1 FY16 (2015-05-08 to 2015-07-31) | 13 | +615.1% | +397.9% to +760.6% | 13 | 13 | +316.8% | 3 |
| latest print Q2 FY16 (2015-08-07 to 2015-10-30) | 13 | +628.6% | +591.3% to +709.7% | 13 | 13 | +386.7% | 0 |
| latest print Q3 FY16 (2015-11-06 to 2015-12-31) | 9 | +519.0% | +456.2% to +616.9% | 9 | 9 | +347.5% | 0 |

- **CHEAP held on all 3 dates, FAIR on none of 24, RICH on none of 26.** Every 2015 entry ($19.20-33.75) returned +333.7% to +760.6% over
  two years (two-year prices $97.67-214.14) and beat SPY by 317-738pp: the three CHEAP entries of July 2015 +683.2% to +760.6%, the RICH
  ones +370.3% to +709.7% (median +584.9%). The two-year lows were the $19.31 of 2015-07-27 (26 dates) and the $25.22 of 2016-02-08
  (14); the drawdowns were 24-25%. Over three years the 2015 dates returned +288.1% to +1,211.8%.
- **The anchor held; the multiple did not.** FY15's $1.12 stood for FY16E and FY2016 earned $1.08, close; the stock's price multiplied
  by four to eight in two years while FY2017 earned $2.57, so the multiple rose with the earnings.
- **Within the year the price ranks nothing** (Spearman -0.05 and +0.23); the proxy composite ranks the two-year return at -0.77 and the
  m12-24 average at -0.72, the wrong sign.
- **The two-year price landed nearest XBULL on all 53 dates.**

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +410.1% | +19.1% to +790.3% | 50 | 52 | +335.3% | 0 |
| FY16E $1.12 (2016-01-08 to 2016-02-12) | 6 | +726.4% | +652.8% to +790.3% | 6 | 6 | +467.5% | 0 |
| FY17E $1.08 (2016-02-19 to 2016-12-30) | 46 | +361.0% | +19.1% to +704.5% | 44 | 46 | +294.6% | 0 |
| latest print Q3 FY16 (2016-01-08 to 2016-02-12) | 6 | +726.4% | +652.8% to +790.3% | 6 | 6 | +467.5% | 0 |
| latest print Q4 FY16 (2016-02-19 to 2016-05-06) | 12 | +579.7% | +503.9% to +704.5% | 12 | 12 | +424.2% | 0 |
| latest print Q1 FY17 (2016-05-13 to 2016-08-05) | 13 | +445.5% | +335.1% to +523.8% | 13 | 13 | +337.1% | 0 |
| latest print Q2 FY17 (2016-08-12 to 2016-11-04) | 13 | +306.0% | +182.7% to +358.7% | 13 | 13 | +257.7% | 0 |
| latest print Q3 FY17 (2016-11-11 to 2016-12-30) | 8 | +62.0% | +19.1% to +135.1% | 6 | 8 | +155.1% | 0 |

- **RICH and AVOID on every date; the call held on none.** The entries ($25.73-109.78, 23-106x the last full year's EPS) returned +19.1%
  to +790.3% over two years (median +410.1%), 50 cleared the hurdle and all beat SPY, by 8.1-743.2pp. The eight entries after the Q3 FY17
  print (2016-11-11 to 2016-12-30, $87.97-109.78) returned least, +19.1% to +135.1%: their windows end in November-December 2018, after
  the stock's fall from the $289.36 of 2018-10-01. Over three years the 2016 dates returned +119.2% to +494.0%.
- **The cheaper the entry, the more it returned:** the entry price ranks the two-year return at Spearman -0.99 (the m12-24 average at
  -0.99), Ratio B at -0.62 and -0.58, the proxy composite at -0.85 and -0.87. The class did not move, so it ranked nothing.
- **The two-year price landed nearest XBULL on all 52 dates.**

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +10.3% | -4.8% to +100.2% | 17 | 19 | +30.1% | 33 |
| FY17E $1.08 (2017-01-06 to 2017-02-03) | 5 | +44.3% | +27.6% to +52.0% | 4 | 5 | +119.7% | 0 |
| FY18E $2.57 (2017-02-10 to 2017-12-29) | 47 | +7.2% | -4.8% to +100.2% | 13 | 14 | +15.4% | 33 |
| latest print Q3 FY17 (2017-01-06 to 2017-02-03) | 5 | +44.3% | +27.6% to +52.0% | 4 | 5 | +119.7% | 0 |
| latest print Q4 FY17 (2017-02-10 to 2017-05-05) | 13 | +65.9% | +31.4% to +100.2% | 12 | 13 | +106.9% | 0 |
| latest print Q1 FY18 (2017-05-11 to 2017-08-04) | 13 | +2.4% | -4.8% to +34.4% | 1 | 1 | +30.9% | 12 |
| latest print Q2 FY18 (2017-08-11 to 2017-11-03) | 13 | -0.4% | -3.8% to +9.9% | 0 | 0 | -3.8% | 13 |
| latest print Q3 FY18 (2017-11-10 to 2017-12-29) | 8 | +11.5% | -3.3% to +23.2% | 0 | 0 | -11.8% | 8 |

- **RICH held on 33 of 52 dates, every one from 2017-05-11.** The 18 entries of January to early May 2017 ($95.49-114.38; FY16's $1.08,
  then FY17's $2.57 from 2017-02-10) returned +27.6% to +100.2% over two years (median +60.2%) and beat SPY by 5.5-71.1pp: the call
  missed. The 34 from 2017-05-11 ($126.50-216.96, 49-84x FY17's $2.57) returned -4.8% to +34.4% (median +0.9%); all but the first
  (2017-05-11, +34.4%, 9.8pp over SPY) lagged SPY and missed the hurdle: their windows end in 2019, after the fall from $289.36 (2018-10-01) to $127.08 (2018-12-24), a drawdown of 56.1%,
  when the Q4 FY19 guide was cut from $2.70 billion to $2.20 billion. Over three years (to the end of 2020) every 2017 date returned
  +106.6% to +225.4% and beat SPY.
- **The anchor was low again.** FY17's $2.57 stood for FY18E; FY2018 earned $4.82 and FY2019 $6.63, FY2020 $4.52.
- **The price and the adjusted gap ranked the outcome; the composite did not.** The entry price ranks the two-year return at Spearman
  -0.75 (the m12-24 average at -0.99), the EPP gap at -0.47 and -0.55, Ratio B at -0.74 and -0.63, the adjusted gap at +0.74 and +0.79,
  the proxy composite at +0.58 and +0.73.
- **The two-year price landed nearest XBULL on 35 dates and BULL on 17.**

## Across 2014-2017

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 8 | +93.0% | +71.2% to +760.6% | 8 | 8 | +56.0% | 8 |
| class FAIR | 60 | +238.0% | +47.8% to +723.3% | 60 | 60 | +104.0% | 0 |
| class RICH | 140 | +307.4% | -4.8% to +790.3% | 103 | 107 | +171.2% | 33 |
| legacy tier BUY | 8 | +93.0% | +71.2% to +389.7% | 8 | 8 | +56.0% | 5 |
| legacy tier ACCUMULATE | 17 | +421.7% | +47.8% to +760.6% | 17 | 17 | +279.0% | 3 |
| legacy tier WATCHLIST | 47 | +231.4% | +87.0% to +709.7% | 47 | 47 | +90.4% | 0 |
| legacy tier AVOID | 136 | +305.4% | -4.8% to +790.3% | 99 | 103 | +166.9% | 33 |

- **The P/E band from the stock's own decade read every rerating as RICH.** CHEAP held on 8 of 8 dates, FAIR on none of 60, RICH on 33 of
  140: 41 of 208 (203 of 522 with 2008-2013). The class rested on the last full GAAP year against the stock's ten-year P/E history, whose
  median stayed at 19-21x; NVIDIA's EPS rose from $0.74 (FY2014) to $2.57 (FY2017) and $4.82 (FY2018), and the stock went from 17-28x the
  trailing year in 2014-2015 to 37-106x in 2016-2017. RICH missed on every date of 2014-2016 and the first months of 2017 and held only
  for the entries whose two-year windows ended after the fall of late 2018. Hypotheses only: for a company whose earnings base shifts, a
  P/E band drawn from its own past marks every rerating RICH, and the RICH call pays only at a cyclical turn; a FAIR call's ±15pp band
  is too narrow for a stock that moves this much (none of 60 held). Test them on other tickers and periods; never fold them into NVDA's
  method or fact sheet.
- **The composite has no stable sign.** The proxy composite ranks the two-year return at +0.80 in 2014, -0.77 in 2015, -0.85 in 2016 and
  +0.58 in 2017.
- **The judgement calls touch few of these dates.** The variants run before any outcome moved classes only in 2014-2015 (every signal at
  BEAR 63, at XBULL 39; the guides unused 16; FY2009 and FY2010 at non-GAAP 12) and none in 2016-2017; DURABLE and the restructuring
  charges added back moved none. The RICH calls of 2016-2017 rest on GAAP EPS of a past year and the stock's own P/E history alone.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY | 5 | +269.6% | +263.4% to +312.6% | 5 | 5 | +161.1% | 0 |
| class RICH, legacy tier ACCUMULATE | 2 | +229.6% | +228.7% to +229.6% | 2 | 2 | +126.2% | 0 |
| class RICH, legacy tier WATCHLIST | 1 | +165.7% | +165.7% to +165.7% | 1 | 1 | +71.0% | 0 |
| class RICH, legacy tier AVOID | 44 | +42.8% | -21.1% to +165.7% | 25 | 33 | -9.6% | 11 |
| FY18E $2.57 (2018-01-05 to 2018-02-02) | 5 | +8.9% | +1.8% to +10.2% | 0 | 0 | -21.6% | 5 |
| FY19E $4.82 (2018-02-09 to 2018-12-28) | 47 | +65.9% | -21.1% to +312.6% | 33 | 41 | +0.1% | 6 |
| latest print Q3 FY18 (2018-01-05 to 2018-02-02) | 5 | +8.9% | +1.8% to +10.2% | 0 | 0 | -21.6% | 5 |
| latest print Q4 FY18 (2018-02-09 to 2018-05-04) | 13 | +17.4% | -21.1% to +31.8% | 0 | 7 | -15.6% | 6 |
| latest print Q1 FY19 (2018-05-11 to 2018-08-10) | 14 | +55.9% | +27.2% to +75.8% | 13 | 14 | -2.7% | 0 |
| latest print Q2 FY19 (2018-08-17 to 2018-11-09) | 13 | +102.1% | +86.0% to +165.7% | 13 | 13 | +15.4% | 0 |
| latest print Q3 FY19 (2018-11-16 to 2018-12-28) | 7 | +264.4% | +228.7% to +312.6% | 7 | 7 | +154.9% | 0 |

- **RICH held on 11 of 52 dates, all before 2018-03-23.** The five entries of January 2018 (FY17's $2.57, $215.40-243.33, 84-95x) and
  the first six after the Q4 FY18 print (to 2018-03-16) returned -21.1% to +20.0% over two years and lagged SPY by 1.5-22.2pp: their
  windows end in early 2020, near the fall from $314.70 (2020-02-19). From 2018-03-23 every entry beat SPY, the later the more: the
  seven after the Q3 FY19 print ($129.57-164.43, entered after the fall that began in October 2018) returned +228.7% to +312.6%. All but
  one of the 52 dates had the $127.08 of 2018-12-24 as their two-year low (drawdowns of 38-56%). Over three years every 2018 date
  returned +104.9% to +808.9% and beat SPY.
- **The anchor rose and fell.** FY18's $4.82 stood for FY19E; FY2019 earned $6.63 and FY2020 $4.52.
- **Little ranked the outcome.** The entry price ranks the two-year return at Spearman -0.16 (the m12-24 average at -0.24), the EPP gap
  at -0.40 and -0.48, Ratio B at -0.42 and -0.52, the adjusted gap at +0.15 and +0.22, the proxy composite at +0.14 and +0.08.
- **The two-year price landed nearest BULL on 45 dates, XBULL on 5 and BASE on 2.**

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier ACCUMULATE | 5 | +488.8% | +403.5% to +516.5% | 5 | 5 | +235.4% | 0 |
| class RICH, legacy tier BUY | 40 | +341.6% | +189.2% to +442.4% | 40 | 40 | +231.8% | 0 |
| class RICH, legacy tier ACCUMULATE | 5 | +353.7% | +228.6% to +493.6% | 5 | 5 | +221.8% | 0 |
| class RICH, legacy tier WATCHLIST | 2 | +423.1% | +363.7% to +423.1% | 2 | 2 | +225.2% | 0 |
| FY19E $4.82 (2019-01-04 to 2019-02-08) | 6 | +267.0% | +228.6% to +290.7% | 6 | 6 | +186.8% | 0 |
| FY20E $6.63 (2019-02-15 to 2019-12-27) | 46 | +385.1% | +189.2% to +516.5% | 46 | 46 | +233.7% | 0 |
| latest print Q3 FY19 (2019-01-04 to 2019-02-08) | 6 | +267.0% | +228.6% to +290.7% | 6 | 6 | +186.8% | 0 |
| latest print Q4 FY19 (2019-02-15 to 2019-05-10) | 13 | +225.0% | +189.2% to +281.2% | 13 | 13 | +169.6% | 0 |
| latest print Q1 FY20 (2019-05-17 to 2019-08-09) | 13 | +386.5% | +262.8% to +427.4% | 13 | 13 | +250.2% | 0 |
| latest print Q2 FY20 (2019-08-16 to 2019-11-08) | 13 | +400.9% | +334.4% to +493.6% | 13 | 13 | +246.8% | 0 |
| latest print Q3 FY20 (2019-11-15 to 2019-12-27) | 7 | +466.9% | +363.7% to +516.5% | 7 | 7 | +233.7% | 0 |

- **No call held: RICH on 47 dates and FAIR on 5, and every entry returned +189.2% to +516.5% over two years**, beating SPY by
  145.0-465.1pp. The entries ($135.46-239.37, 20-36x the last full year) included the 40 BUY-tier dates of January to October 2019,
  whose class said RICH while their Ratio B was 0.28-0.84; the five FAIR dates of November-December 2019 returned +403.5% to +516.5%. Over
  three years the 2019 dates returned +139.3% to +761.7%.
- **The anchor fell, and the stock did not follow it.** FY19's $6.63 stood for FY20E; FY2020 earned $4.52, and FY2021 $6.90.
- **The adjusted gap and the composite had the right sign, weakly:** +0.48 and +0.45 against the two-year return (+0.40 and +0.10 against
  the m12-24 average); the entry price +0.26 and -0.13, Ratio B +0.14 and -0.33.
- **The two-year price landed nearest BULL on 26 dates and XBULL on 26.**

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier ACCUMULATE | 1 | +287.0% | +287.0% to +287.0% | 1 | 1 | +246.3% | 0 |
| class RICH, legacy tier WATCHLIST | 5 | +332.8% | +273.7% to +410.9% | 5 | 5 | +225.1% | 0 |
| class RICH, legacy tier AVOID | 47 | +62.1% | -18.5% to +414.9% | 28 | 37 | +119.4% | 10 |
| FY20E $6.63 (2020-01-03 to 2020-02-07) | 6 | +332.8% | +273.7% to +410.9% | 6 | 6 | +229.1% | 0 |
| FY21E $4.52 (2020-02-14 to 2020-12-31) | 47 | +62.1% | -18.5% to +414.9% | 28 | 37 | +119.4% | 10 |
| latest print Q3 FY20 (2020-01-03 to 2020-02-07) | 6 | +332.8% | +273.7% to +410.9% | 6 | 6 | +229.1% | 0 |
| latest print Q4 FY20 (2020-02-14 to 2020-05-15) | 14 | +245.3% | +108.9% to +414.9% | 14 | 14 | +222.7% | 0 |
| latest print Q1 FY21 (2020-05-22 to 2020-08-14) | 13 | +71.4% | +51.4% to +112.3% | 13 | 13 | +139.9% | 0 |
| latest print Q2 FY21 (2020-08-21 to 2020-11-13) | 13 | +8.3% | -18.5% to +41.0% | 1 | 3 | +67.9% | 10 |
| latest print Q3 FY21 (2020-11-20 to 2020-12-31) | 7 | +22.9% | +12.2% to +30.9% | 0 | 7 | +45.2% | 0 |

- **RICH held on 10 of 53 dates, all after the Q2 FY21 print.** The entries of 2020-09-04 to 2020-11-06 ($486.58-582.48, 108-129x FY20's
  $4.52) returned -18.5% to +18.5% over two years and lagged SPY by 6.6-24.9pp: their windows end in the fall of 2022, at or near the low
  of 2022-10-14 ($112.27 after the split, $449.08 on their basis), a drawdown of up to 66%. The entries of January to mid-May 2020
  ($205.75-339.63) returned +108.9% to +414.9%, those of May to August +51.4% to +112.3%; all of them beat SPY. Over three years every 2020
  date returned +143.4% to +404.5% and beat SPY.
- **The anchor was low.** FY20's $4.52 stood for FY21E; FY2021 earned $6.90 ($1.725 after the split).
- **The price ranked the outcome.** The entry price ranks the two-year return at Spearman -0.95 (the m12-24 average at -0.97), the EPP
  gap at -0.95 and -0.97, Ratio B at -0.75 and -0.72, the adjusted gap at +0.92 and +0.90, the proxy composite at +0.37 and +0.44.
- **The two-year price landed nearest XBULL on 34 dates and BULL on 19.**

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +93.8% | +12.2% to +150.5% | 49 | 52 | +21.5% | 0 |
| FY21E $4.52 (2021-01-08 to 2021-02-19) | 7 | +42.3% | +12.2% to +57.0% | 4 | 7 | +31.2% | 0 |
| FY22E $6.90 (2021-02-26 to 2021-07-16) | 21 | +101.3% | +68.4% to +150.5% | 21 | 21 | +22.7% | 0 |
| FY22E $1.725 (2021-07-23 to 2021-12-31) | 24 | +100.6% | +49.6% to +139.9% | 24 | 24 | +20.2% | 0 |
| latest print Q3 FY21 (2021-01-08 to 2021-02-19) | 7 | +42.3% | +12.2% to +57.0% | 4 | 7 | +31.2% | 0 |
| latest print Q4 FY21 (2021-02-26 to 2021-05-21) | 13 | +92.0% | +68.4% to +108.8% | 13 | 13 | +28.0% | 0 |
| latest print Q1 FY22 (2021-05-28 to 2021-08-13) | 12 | +123.9% | +102.5% to +150.5% | 12 | 12 | +16.9% | 0 |
| latest print Q2 FY22 (2021-08-20 to 2021-11-12) | 13 | +102.9% | +51.4% to +119.8% | 13 | 13 | +21.7% | 0 |
| latest print Q3 FY22 (2021-11-19 to 2021-12-31) | 7 | +57.4% | +49.6% to +76.0% | 7 | 7 | +15.0% | 0 |

- **RICH and AVOID on every date; the call held on none.** The entries ($498.46-819.48 before the split, $194.99-329.85 after it; 72-191x
  the last full year) returned +12.2% to +150.5% over two years and beat SPY, which returned -7.8% to +12.9%, by 7.2-143.5pp; 49 cleared
  the hurdle. Their windows end in 2023, after the low of 2022-10-14 ($112.27, a drawdown of 63-66%) and the rise that followed. Over three
  years (to the end of 2024, after the ten-for-one split of 2024-06-10, restated) every 2021 date returned +293.9% to +627.7%.
- **The anchor was low again.** FY21's $6.90 ($1.725 after the split) stood for FY22E; FY2022 earned $3.85 a share on the split basis
  (Q4 FY22 release, 2022-02-16).
- **Nothing ranked the outcome:** the entry price at -0.01 and -0.23, the EPP gap at -0.41 and -0.36, the adjusted gap at +0.55 and +0.15,
  the proxy composite at +0.11 and -0.28.
- **The two-year price landed nearest XBULL on 37 dates and BULL on 15.**

## Across 2018-2021

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 5 | +488.8% | +403.5% to +516.5% | 5 | 5 | +235.4% | 0 |
| class RICH | 204 | +102.7% | -21.1% to +493.6% | 163 | 183 | +54.0% | 21 |
| legacy tier BUY | 45 | +312.6% | +189.2% to +442.4% | 45 | 45 | +221.8% | 0 |
| legacy tier ACCUMULATE | 13 | +403.5% | +228.6% to +516.5% | 13 | 13 | +229.6% | 0 |
| legacy tier WATCHLIST | 8 | +349.1% | +165.7% to +423.1% | 8 | 8 | +225.1% | 0 |
| legacy tier AVOID | 143 | +69.8% | -21.1% to +414.9% | 102 | 122 | +24.3% | 21 |

- **RICH held on 21 of 204 dates, FAIR on none of 5: 21 of 209 (224 of 731 with 2008-2017).** As in 2014-2017, the P/E band drawn from
  the stock's own decade (median 19.7-26.1x) put every date of a stock trading at 20-191x the last full year in RICH or, at its lowest
  in 2019, FAIR. The RICH call held only for the entries whose two-year windows ended at a cyclical low: those of January to mid-March
  2018 (windows ending near the fall of February-March 2020) and of September to early November 2020 (windows ending at the low of
  October 2022). Every other entry, including all 52 of 2019 and all 52 of 2021, beat SPY. Hypotheses only, the same as for 2014-2017: a
  P/E band from the stock's own past marks a rerating RICH throughout and pays only at a cyclical turn. Test them on other tickers and
  periods; never fold them into NVDA's method or fact sheet.
- **The legacy tier diverged from the class at the 2018-2019 low.** From the Q3 FY19 print to October 2019 the class stayed RICH while
  Ratio B (0.28-0.92) put the tier at BUY or ACCUMULATE on 52 dates; those entries returned +189.2% to +493.6% over two years.
- **The composite has no stable sign:** +0.14 in 2018, +0.45 in 2019, +0.37 in 2020 and +0.11 in 2021 against the two-year return.
- **The judgement calls touch few of these dates.** The variants run before any 2018-2021 outcome moved 52 classes at XBULL signals (all
  in 2018-11-16 to 2019-11-08, RICH to FAIR), 5 at BEAR, 15 without the guides and 3 with FY2009 and FY2010 at non-GAAP, and none after
  2020-01-31; the January 2019 update and DURABLE moved none.
