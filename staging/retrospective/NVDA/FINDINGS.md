# NVDA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NVDA weekly dates: 105 from 2008-01-04 to 2009-12-31, all NVIDIA Corporation (Nasdaq: NVDA).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build was committed and pushed (2008-2009: 9510254, firewall result 99a5d02); the outcomes were computed on 2026-11-12.
Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31). Prices are on the AS_OF share basis (no split falls
in any horizon; the next is 2021's), so every price is as traded. NVIDIA paid no dividend until November 2012: its first ($0.075 a
share on this basis, ex-date 2012-11-20) falls only inside the three-year horizon of the dates from 2009-11-20 on. Medians of an even
count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three.
"Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the
benchmark, and RICH should miss the hurdle and lag the benchmark.

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
