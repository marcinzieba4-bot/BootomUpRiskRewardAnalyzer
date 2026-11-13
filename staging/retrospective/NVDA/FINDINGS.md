# NVDA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NVDA weekly dates: 314 from 2008-01-04 to 2013-12-31, all NVIDIA Corporation (Nasdaq: NVDA).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 9510254, firewall result 99a5d02; 2010-2013: 69a20a9, firewall result
858dc95); the outcomes were computed on 2026-11-12 (2008-2009) and 2026-11-13 (2010-2013). Every date has its 6-month, 1-, 2- and
3-year horizons (the last ends 2016-12-31). Prices are on the AS_OF share basis (no split falls in any horizon; the next is 2021's),
so every price is as traded. NVIDIA paid no dividend until November 2012: its first ($0.075 a share on this basis, ex-date 2012-11-20)
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
