# PFE retrospective findings (hindsight)

Patterns seen in `outcome.json` for the PFE weekly dates: 732 from 2008-01-04 to 2021-12-31, all Pfizer Inc (NYSE: PFE). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time
build was committed and pushed (40abcf7 for 2008-2009, e054737 for 2010-2013, 0f08467 for 2014-2017, 0ce7593 for 2018-2021). Outcomes
were computed on 2026-11-10 from the closes posted to 2026-11-09 (2008-2013) and 2026-11-10 (2014-2021); every date has its 6-month, 1-,
2- and 3-year horizons (the last ends 2024-12-31). Total returns include the dividends paid in each horizon; the prices are on the
as-traded basis of the models (Yahoo's series times its 1.054 factor of 2020-11-17, for the dates before that day: a horizon that
crosses it counts the Upjohn/Viatris distribution as if it were a split, the tool's standing treatment, so the distributed Viatris
shares stay in the holding (the MAR rule for outcomes); dates from 2020-11-17 use Yahoo's series as it is, the price as traded). Medians
of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over
three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of it,
and RICH should miss the hurdle and lag it.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 50 | -7.1% | -12.9% to +26.3% | 0 | 30 | -9.4% | 30 |
| class RICH, legacy tier AVOID | 3 | -8.0% | -12.9% to -4.1% | 0 | 3 | -31.1% | 0 |
| FY07E $1.055 (2008-01-04 to 2008-01-18) | 3 | -8.0% | -12.9% to -4.1% | 0 | 3 | -31.1% | 0 |
| FY08E $1.855 (2008-01-24 to 2008-04-11) | 12 | -9.0% | -12.5% to -6.2% | 0 | 9 | -23.8% | 9 |
| FY08E $1.805 (2008-04-18 to 2008-10-17) | 27 | -7.7% | -12.9% to +26.3% | 0 | 21 | -9.4% | 21 |
| FY08E $1.66 (2008-10-22 to 2008-12-31) | 11 | +10.2% | +7.2% to +16.9% | 0 | 0 | +0.6% | 0 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | -8.0% | -12.9% to -4.1% | 0 | 3 | -31.1% | 0 |
| latest print Q4 2007 (2008-01-24 to 2008-04-11) | 12 | -9.0% | -12.5% to -6.2% | 0 | 9 | -23.8% | 9 |
| latest print Q1 2008 (2008-04-18 to 2008-07-18) | 14 | -7.8% | -12.0% to -1.8% | 0 | 14 | -7.6% | 14 |
| latest print Q2 2008 (2008-07-24 to 2008-10-17) | 13 | -2.1% | -12.9% to +26.3% | 0 | 7 | -9.4% | 7 |
| latest print Q3 2008 (2008-10-22 to 2008-12-31) | 11 | +10.2% | +7.2% to +16.9% | 0 | 0 | +0.6% | 0 |

- **CHEAP held on 30 of 50 dates, every one by beating SPY, none by clearing the hurdle.** The 37 CHEAP dates from 2008-01-24 to
  2008-10-03 ($17.28-23.59) returned -12.9% to +2.1% over two years, dividends included, while SPY returned -18.7% to +8.0%; 30 of them
  beat it, by up to 11.9pp, the other 7 lagged by up to 8.8pp. The 13 dates from 2008-10-10 ($15.14-17.71) returned +7.2% to +26.3% but
  lagged SPY's rebound (+27.0% to +56.9%) by 10.5-40.0pp. Every 2008 date sat through a 36-52% drawdown; the low close was $11.66 on
  2009-03-02, 7.0x FY08's $1.66 guide and 8.2x the first FY09 guide. Over three years (to the end of 2011) the 2008 dates returned
  -12.5% to +41.2% (median +15.0%) and 29 beat SPY; none cleared the three-year hurdle.
- **The floor was far above where the stock bottomed.** The EPP floor was 17x the reported-EPS guide ($28-32) on every 2008 date after
  the Q4 2007 print, set by the calendar-year lows of 2004-2007 (14.7-20.2x), which are GAAP multiples on years carrying $0.43 (2006) and $0.36
  (2007) a share of purchase-accounting adjustments, mostly recurring amortization, and the charges of the Pharmacia integration and the
  cost programmes. The price was already 25-51% under
  that floor and then fell to $11.66. The same pattern as RCL, MAR and BKR in early 2008: a floor from a window's earlier multiples, here
  without a cycle in the earnings. Hypothesis, not a rule: test a floor that discounts a window's own trend in multiples (the stock's
  P/E fell from 2004 to 2008 on a shrinking U.S. franchise) on other tickers and periods; never fit it to PFE's outcomes.
- **January 2008's RICH dates were right on the price and wrong on the test.** On FY07's depressed $1.055 the three dates ($22.50-24.02)
  were 21-23x and above a 20x floor; the stock lost 4-13% over two years and its m12-24 average price sat 30-34% under the entry, but
  SPY fell further (-10% to -16%), so RICH "lagging the benchmark" failed on all three. Under the alternative reading of the 2003
  exclusion (a ten-year window, retro/README.md "PFE") they would have been CHEAP and held. That is a hindsight observation about one
  judgement call, never a reason to re-encode it.
- **Entry price ranks the outcome, as in every one-stock crash.** Across the 53 dates the entry price ranks the return to the m12-24
  average price at Spearman -1.00 and the two-year return at -0.76; the EPP gap at -0.94; the proxy composite at +0.62 and the adjusted
  gap at +0.60 (the right signs). Ratio B ranks it at -0.31.
- **The two-year price landed nearest BEAR on 50 dates and BASE on 3,** at 1.05-2.17 times the BEAR price and 0.31-0.70 times BULL.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 51 | +29.9% | +9.4% to +66.6% | 25 | 21 | +16.0% | 39 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +15.5% | +15.5% | 0 | 0 | +6.5% | 0 |
| FY08E $1.66 (2009-01-09 to 2009-01-23) | 3 | +13.9% | +13.5% to +13.9% | 0 | 0 | -4.2% | 0 |
| FY09E $1.415 (2009-01-27 to 2009-04-24) | 13 | +54.9% | +26.4% to +65.4% | 12 | 2 | +22.3% | 12 |
| FY09E $1.275 (2009-04-29 to 2009-07-17) | 12 | +49.0% | +41.6% to +66.6% | 12 | 5 | +21.2% | 12 |
| FY09E $1.375 (2009-07-23 to 2009-10-16) | 13 | +18.9% | +15.1% to +33.2% | 1 | 8 | +14.7% | 9 |
| FY09E $1.475 (2009-10-21 to 2009-12-31) | 11 | +22.3% | +9.4% to +27.3% | 0 | 6 | +5.9% | 6 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +13.9% | +13.5% to +13.9% | 0 | 0 | -4.2% | 0 |
| latest print Q4 2008 (2009-01-27 to 2009-04-24) | 13 | +54.9% | +26.4% to +65.4% | 12 | 2 | +22.3% | 12 |
| latest print Q1 2009 (2009-04-29 to 2009-07-17) | 12 | +49.0% | +41.6% to +66.6% | 12 | 5 | +21.2% | 12 |
| latest print Q2 2009 (2009-07-23 to 2009-10-16) | 13 | +18.9% | +15.1% to +33.2% | 1 | 8 | +14.7% | 9 |
| latest print Q3 2009 (2009-10-21 to 2009-12-31) | 11 | +22.3% | +9.4% to +27.3% | 0 | 6 | +5.9% | 6 |

- **CHEAP held on 39 of 52 dates.** The 25 dates from the Q4 2008 print (2009-01-27, the day after the Wyeth deal and the dividend cut)
  to 2009-07-17 ($12.31-15.82) returned +26.4% to +66.6%, 24 of them clearing the hurdle. The three dates of January 2009 before that
  print ($17.4-17.5) returned +13.5-13.9% and lagged SPY's rebound by 34-46pp; the 24 dates from 2009-07-23 ($15.77-18.60) returned +9.4%
  to +33.2%, clearing the hurdle once and beating SPY on 14. Only 21 dates beat SPY over two years: SPY's run from the March 2009 low
  outpaced the stock's.
- **The three-year read is stronger, unlike BKR's.** Measured to January-December 2012, the 2009 dates returned +37.7% to +90.7% (median
  +63.2%); 42 cleared the three-year hurdle (+52.1%) and 40 beat SPY, so 48 of 52 held at three years against 39 at two.
- **The class never moved while the inputs did.** Through 2009 the reported-EPS guide went from $1.34-1.49 to $1.20-1.35 and back up to
  $1.45-1.50, BASE from +3.3% to -3.8% and then +5.6%/yr and the proxy composite from 2.45 to 1.80 and then 2.10, and the price state stayed CHEAP: the price was 14-42%
  under a 15x floor on every date. Within the year the entry price ranks the return to the m12-24 average price at Spearman -0.92 and the
  two-year return at -0.88; the proxy composite ranks them at -0.74 and -0.79, the wrong sign, which is the calendar (the later prints were
  both stronger and higher-priced entries), not evidence against the signals.
- **The two-year price landed nearest BASE on 39 dates and BEAR on 13,** at 0.51-0.90 times the BASE price and 0.44-0.77 times BULL.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +53.3% | +19.9% to +74.0% | 43 | 47 | +27.5% | 47 |
| FY09E $1.475 (2010-01-08 to 2010-01-29) | 4 | +23.5% | +19.9% to +23.6% | 0 | 2 | +4.9% | 2 |
| FY10E $1.025 (2010-02-04 to 2010-10-29) | 39 | +53.3% | +26.2% to +74.0% | 34 | 36 | +26.7% | 36 |
| FY10E $0.89 (2010-11-03 to 2010-12-31) | 9 | +53.7% | +48.9% to +60.1% | 9 | 9 | +35.0% | 9 |
| latest print Q3 2009 (2010-01-08 to 2010-01-29) | 4 | +23.5% | +19.9% to +23.6% | 0 | 2 | +4.9% | 2 |
| latest print Q4 2009 (2010-02-04 to 2010-04-30) | 13 | +36.9% | +26.2% to +46.3% | 8 | 10 | +17.3% | 10 |
| latest print Q1 2010 (2010-05-05 to 2010-07-30) | 13 | +59.2% | +38.3% to +74.0% | 13 | 13 | +38.5% | 13 |
| latest print Q2 2010 (2010-08-04 to 2010-10-29) | 13 | +55.3% | +50.4% to +60.5% | 13 | 13 | +27.4% | 13 |
| latest print Q3 2010 (2010-11-03 to 2010-12-31) | 9 | +53.7% | +48.9% to +60.1% | 9 | 9 | +35.0% | 9 |

- **CHEAP held on 47 of 52 dates.** Over two years the 2010 dates returned +19.9% to +74.0% (median +53.3%) against SPY's +15.7% to
  +38.6%; 43 cleared the hurdle and 47 beat SPY, by up to 45.8pp. The five failures are 2010-01-22 to 2010-02-19 ($17.99-18.96): +23.3%
  to +27.0%, under the hurdle and 0.6-4.7pp behind SPY. Every date sat through a 22-29% drawdown (the low close $14.14 on 2010-07-02),
  and the entries of late May to July 2010 ($14.14-15.46) returned the most (+53.3% to +74.0%).
- **The three-year read is cleaner.** Over three years (to January-December 2013) the 2010 dates returned +48.9% to +119.1% (median +90.3%); all 52 beat
  SPY and 51 cleared the three-year hurdle.
- **The class rested on Wyeth in growth, and that held.** BASE was +37.6%/yr from the FY2010 revenue guide read on the Pfizer-only
  FY2009. Read on the FY2009 10-K's pro forma combined year (the sensitivity in retro/README.md, "PFE 2010-2013"), 33 of the 2010 dates
  become FAIR or RICH, and 28 of them, which cleared the hurdle or beat SPY, would have failed. The stock entered 2010 at 12.7-19.8x the
  reported-EPS guide; the two-year price landed nearest BASE on 45 dates and BEAR on 7, at 0.57-0.79 times the BASE price.
- **Rankings had the right signs except the floor gap.** Within the year the entry price ranks the return to the m12-24 average price at
  Spearman -0.79 and the two-year return at -0.78; the adjusted gap at +0.59 and +0.72, the proxy composite at +0.57 and +0.70, Ratio B
  at -0.44 and -0.50, and the EPP gap at +0.33 and +0.31 (the wrong sign: the dates nearest the floor came before the Q4 2009 print).

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 4 | +55.0% | +50.8% to +57.1% | 4 | 4 | +27.6% | 4 |
| class FAIR, legacy tier WATCHLIST | 3 | +73.3% | +68.8% to +84.2% | 3 | 3 | +44.8% | 0 |
| class RICH, legacy tier AVOID | 39 | +52.6% | +41.6% to +69.3% | 39 | 37 | +28.8% | 0 |
| class RICH, legacy tier WATCHLIST | 6 | +72.9% | +68.1% to +75.4% | 6 | 6 | +53.1% | 0 |
| FY10E $0.89 (2011-01-07 to 2011-01-28) | 4 | +55.0% | +50.8% to +57.1% | 4 | 4 | +27.6% | 4 |
| FY11E $1.165 (2011-02-02 to 2011-10-28) | 39 | +53.9% | +41.6% to +75.4% | 39 | 39 | +28.8% | 0 |
| FY11E $1.25 (2011-11-02 to 2011-12-30) | 9 | +65.5% | +47.5% to +84.2% | 9 | 7 | +40.7% | 0 |
| latest print Q3 2010 (2011-01-07 to 2011-01-28) | 4 | +55.0% | +50.8% to +57.1% | 4 | 4 | +27.6% | 4 |
| latest print Q4 2010 (2011-02-02 to 2011-04-29) | 13 | +51.4% | +46.8% to +65.6% | 13 | 13 | +22.7% | 0 |
| latest print Q1 2011 (2011-05-04 to 2011-07-29) | 13 | +48.6% | +41.6% to +62.6% | 13 | 13 | +28.8% | 0 |
| latest print Q2 2011 (2011-08-03 to 2011-10-28) | 13 | +68.1% | +62.6% to +75.4% | 13 | 13 | +49.4% | 0 |
| latest print Q3 2011 (2011-11-02 to 2011-12-30) | 9 | +65.5% | +47.5% to +84.2% | 9 | 7 | +40.7% | 0 |

- **RICH failed on all 45 dates.** From the Q4 2010 print (2011-02-02, $17.45-21.83) the stock returned +41.6% to +75.4% over two years,
  cleared the hurdle on every date and beat SPY on 43 (SPY +16.9% to +55.2%); the m12-24 average price sat 20-56% above the entry. The
  three FAIR dates of November 2011 beat SPY by 21-24pp, outside FAIR's ±15pp. Only the four January CHEAP dates held. At three years
  (to 2014) the 2011 dates returned +52.8% to +88.4%, all above the hurdle, and no RICH date held.
- **The two-year price landed nearest BULL on 28 dates and XBULL on 20,** at 0.70-1.29 times the BULL price: BULL here was the FY04-FY10
  EPS CAGR (-2.2% to -3.3%/yr) at the window's 75th-percentile P/E, so the stock rerated while the reported EPS guides fell.
- **What the call stood on.** On the reported-EPS guide ($1.165, then $1.25 with the Capsugel gain) the stock was 14.8-18.0x, near its
  window's median, while the company's adjusted EPS guide ($2.16-2.29), which removes $0.59-0.62 a share of purchase-accounting impacts (mostly
  recurring amortization) as well as one-offs, put it at 8-10x. Read on the adjusted figures throughout (the README sensitivity), 48 of the 2011 dates
  move to CHEAP or FAIR and 29 of them would have held. Hypothesis, not a rule: GAAP EPS that carries large recurring amortization and
  frequent one-offs may misplace a serial acquirer in its own P/E history; test an EPS that adds back only the after-tax amortization of
  acquired intangibles on other tickers and periods, never fit to PFE's outcomes. The house rule (recurring amortization keeps GAAP)
  stands until a new method version says otherwise.
- **Rankings.** The entry price ranks the return to the m12-24 average price at -0.62 and the two-year return at -0.69; the EPP gap at
  -0.79 and -0.76 and Ratio B at -0.58 and -0.66 (the right signs); the proxy composite at -0.38 and -0.20 (the wrong sign).

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 43 | +35.3% | +15.6% to +52.4% | 27 | 9 | +27.3% | 16 |
| class RICH, legacy tier WATCHLIST | 9 | +58.4% | +45.3% to +59.9% | 9 | 9 | +38.5% | 0 |
| FY11E $1.25 (2012-01-06 to 2012-01-27) | 4 | +50.2% | +46.6% to +50.4% | 4 | 4 | +34.6% | 0 |
| FY12E $1.445 (2012-02-01 to 2012-04-27) | 13 | +52.4% | +41.4% to +59.9% | 13 | 13 | +37.4% | 0 |
| FY12E $1.305 (2012-05-02 to 2012-08-10) | 15 | +39.1% | +26.6% to +45.8% | 13 | 1 | +32.7% | 2 |
| FY12E $1.285 (2012-08-17 to 2012-10-26) | 11 | +28.6% | +15.6% to +32.0% | 0 | 0 | +24.0% | 11 |
| FY12E $1.34 (2012-11-02 to 2012-12-28) | 9 | +32.5% | +30.0% to +35.5% | 6 | 0 | +21.7% | 3 |
| latest print Q3 2011 (2012-01-06 to 2012-01-27) | 4 | +50.2% | +46.6% to +50.4% | 4 | 4 | +34.6% | 0 |
| latest print Q4 2011 (2012-02-01 to 2012-04-27) | 13 | +52.4% | +41.4% to +59.9% | 13 | 13 | +37.4% | 0 |
| latest print Q1 2012 (2012-05-02 to 2012-07-27) | 13 | +39.5% | +34.7% to +45.8% | 13 | 1 | +32.8% | 0 |
| latest print Q2 2012 (2012-08-01 to 2012-10-26) | 13 | +28.6% | +15.6% to +32.0% | 0 | 0 | +25.2% | 13 |
| latest print Q3 2012 (2012-11-02 to 2012-12-28) | 9 | +32.5% | +30.0% to +35.5% | 6 | 0 | +21.7% | 3 |

- **RICH held on 16 of 52 dates, all from the Q2 2012 print.** The 30 dates from 2012-01-06 to 2012-07-27 ($21.05-23.83) returned +34.7%
  to +59.9% over two years, every one above the hurdle; the 16 that held (2012-08-01 to 2012-11-09 and 2012-12-14, $23.79-25.76)
  returned +15.6% to +32.1%, under the hurdle and 8-22pp behind SPY's +36% to +52%. Six dates of November-December cleared the hurdle by
  0.1-3.3pp (2012-11-23 by 0.1pp) while lagging SPY. At three years 11 held.
- **The two-year price landed at or above the BULL price on 51 dates** (1.03-1.23 times it) and nearest XBULL on one: the negative
  history CAGR (-3.6%/yr) put BULL just above the entry price, which is what lifted Ratio B to 1.4-70, and the stock went past it.
- **Rankings had the right signs throughout.** The entry price ranks the return to the m12-24 average price at Spearman -0.99 and the
  two-year return at -0.90; the EPP gap at -0.85 and -0.80, Ratio B at -0.94 and -0.92, the adjusted gap at +0.94 and +0.86, the proxy
  composite at +0.22 and +0.33. The calls that held were the highest entries.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 23 | +18.2% | +6.9% to +32.0% | 0 | 7 | +11.0% | 7 |
| class RICH, legacy tier AVOID | 30 | +27.6% | +19.4% to +35.3% | 4 | 1 | +10.6% | 26 |
| FY12E $1.34 (2013-01-04 to 2013-01-25) | 4 | +30.7% | +27.6% to +31.1% | 0 | 0 | +14.4% | 4 |
| FY13E $1.575 (2013-01-30 to 2013-04-26) | 13 | +27.7% | +19.4% to +34.4% | 3 | 0 | +8.7% | 10 |
| FY13E $1.515 (2013-05-01 to 2013-07-26) | 13 | +26.5% | +23.7% to +35.3% | 1 | 1 | +10.3% | 12 |
| FY13E $3.145 (2013-07-31 to 2013-10-25) | 13 | +23.1% | +17.8% to +32.0% | 0 | 7 | +14.1% | 7 |
| FY13E $3.10 (2013-10-30 to 2013-12-31) | 10 | +13.1% | +6.9% to +16.2% | 0 | 0 | +7.9% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-01-25) | 4 | +30.7% | +27.6% to +31.1% | 0 | 0 | +14.4% | 4 |
| latest print Q4 2012 (2013-01-30 to 2013-04-26) | 13 | +27.7% | +19.4% to +34.4% | 3 | 0 | +8.7% | 10 |
| latest print Q1 2013 (2013-05-01 to 2013-07-26) | 13 | +26.5% | +23.7% to +35.3% | 1 | 1 | +10.3% | 12 |
| latest print Q2 2013 (2013-07-31 to 2013-10-25) | 13 | +23.1% | +17.8% to +32.0% | 0 | 7 | +14.1% | 7 |
| latest print Q3 2013 (2013-10-30 to 2013-12-31) | 10 | +13.1% | +6.9% to +16.2% | 0 | 0 | +7.9% | 0 |

- **RICH held on 26 of 30 dates; the CHEAP calls on the Zoetis-gain guide held on 7 of 23.** The RICH dates of January-July 2013
  ($25.96-31.06) returned +19.4% to +35.3% against SPY's +27.5% to +45.3%; four (2013-02-15 to 2013-05-31) cleared the hurdle by up to
  3.1pp. From the Q2 2013 print, on FY13E $3.145 and $3.10 with the $1.56 and $1.55 Zoetis gain, the stock ($28.21-32.20) was 9-10x and
  called CHEAP: it returned +6.9% to +32.0%, cleared the hurdle on no date and beat SPY on 7 (2013-08-09 to 2013-10-11, by 0.3-2.5pp).
  At three years (to 2016) no 2013 date cleared the hurdle; 24 RICH dates and one CHEAP date held.
- **The gain carried the CHEAP class.** Without it (the reconciliation's "Discontinued operations" line out of the guide, or the Q1 2013
  guide standing; the README sensitivity) the 23 dates are RICH, and 16 of them would have held where 7 CHEAP calls did (net +9).
  Hypothesis, not a rule: a current-year guide whose reported EPS doubles on a one-time gain (1.9 times the EPS without the gain and the
  reconciliation's other one-offs, under the r2 mirror test's "over double") may mislead the multiple; test a guide-level distortion test on
  other tickers and periods, never fit to PFE.
- **Rankings were turned by the class split.** The entry price ranks the return to the m12-24 average price at -0.70 and the two-year
  return at -0.79; the EPP gap, Ratio B, adjusted gap and proxy composite rank the two-year return at +0.35, +0.32, -0.42 and -0.58, the
  wrong signs, because the gain-inclusive CHEAP dates of the second half were both the cheapest-looking and the weakest.
- **The two-year price landed nearest BULL on 27 dates, BASE on 23 and XBULL on 3**: the CHEAP dates nearest BASE at 0.73-0.83 times
  the gain-inclusive BASE price.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 4 | +9.2% | +6.0% to +12.8% | 0 | 0 | +10.5% | 0 |
| class RICH, legacy tier AVOID | 48 | +18.2% | -1.4% to +32.8% | 1 | 28 | +9.7% | 20 |
| FY13E $3.10 (2014-01-03 to 2014-01-24) | 4 | +9.2% | +6.0% to +12.8% | 0 | 0 | +10.5% | 0 |
| FY14E $1.645 (2014-01-29 to 2014-05-02) | 14 | +2.4% | -1.4% to +15.2% | 0 | 0 | +6.1% | 14 |
| FY14E $1.65 (2014-05-06 to 2014-07-25) | 12 | +24.4% | +21.5% to +29.2% | 0 | 12 | +10.2% | 0 |
| FY14E $1.545 (2014-07-30 to 2014-12-26) | 22 | +20.9% | +6.0% to +32.8% | 1 | 16 | +11.9% | 6 |
| latest print Q3 2013 (2014-01-03 to 2014-01-24) | 4 | +9.2% | +6.0% to +12.8% | 0 | 0 | +10.5% | 0 |
| latest print Q4 2013 (2014-01-29 to 2014-05-02) | 14 | +2.4% | -1.4% to +15.2% | 0 | 0 | +6.1% | 14 |
| latest print Q1 2014 (2014-05-06 to 2014-07-25) | 12 | +24.4% | +21.5% to +29.2% | 0 | 12 | +10.2% | 0 |
| latest print Q2 2014 (2014-07-30 to 2014-10-24) | 13 | +25.0% | +18.2% to +32.8% | 1 | 13 | +13.2% | 0 |
| latest print Q3 2014 (2014-10-29 to 2014-12-26) | 9 | +10.1% | +6.0% to +16.0% | 0 | 3 | +6.0% | 6 |

- **The January 2014 CHEAP calls failed, like the gain-inclusive CHEAP calls of late 2013.** On FY13E $3.10 with the Zoetis gain the four
  dates ($30.09-31.09, 9.7-10.0x) returned +6.0% to +12.8% over two years and lagged SPY on all four.
- **RICH held on 20 of 48, and the split was the entry window.** The 14 dates from the Q4 2013 print to 2014-05-02 ($29.86-32.43) returned
  -1.4% to +15.2% and lagged SPY: all held. The 25 dates from 2014-05-06 to 2014-10-24 ($27.83-30.73), on FY13's $1.65 while the reported
  guide was withdrawn and then on $1.545, returned +18.2% to +32.8% and beat SPY on all 25: none held. The Q3 2014 dates held on 6 of 9.
  Over three years no 2014 date cleared the hurdle and 45 of 52 held.
- **Entry price ranks the outcome** at -0.96 against the return to the m12-24 average price and -0.81 against the two-year return; the
  EPP gap at -0.54 and -0.50, the proxy composite at -0.50 and -0.72.
- **The two-year price landed nearest BULL on 37 dates and BASE on 15.**

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +6.8% | -0.6% to +23.8% | 0 | 0 | -1.3% | 53 |
| FY14E $1.545 (2015-01-02 to 2015-01-23) | 4 | +9.6% | +4.1% to +11.1% | 0 | 0 | +1.4% | 4 |
| FY15E $1.445 (2015-01-28 to 2015-04-24) | 13 | +5.6% | +1.0% to +8.1% | 0 | 0 | -2.9% | 13 |
| FY15E $1.395 (2015-04-29 to 2015-07-24) | 13 | +4.2% | -0.6% to +7.9% | 0 | 0 | -1.8% | 13 |
| FY15E $1.425 (2015-07-29 to 2015-10-23) | 13 | +11.7% | -0.6% to +19.0% | 0 | 0 | -0.2% | 13 |
| FY15E $1.40 (2015-10-28 to 2015-12-31) | 10 | +17.6% | +7.3% to +23.8% | 0 | 0 | +4.3% | 10 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +9.6% | +4.1% to +11.1% | 0 | 0 | +1.4% | 4 |
| latest print Q4 2014 (2015-01-28 to 2015-04-24) | 13 | +5.6% | +1.0% to +8.1% | 0 | 0 | -2.9% | 13 |
| latest print Q1 2015 (2015-04-29 to 2015-07-24) | 13 | +4.2% | -0.6% to +7.9% | 0 | 0 | -1.8% | 13 |
| latest print Q2 2015 (2015-07-29 to 2015-10-23) | 13 | +11.7% | -0.6% to +19.0% | 0 | 0 | -0.2% | 13 |
| latest print Q3 2015 (2015-10-28 to 2015-12-31) | 10 | +17.6% | +7.3% to +23.8% | 0 | 0 | +4.3% | 10 |

- **RICH held on all 53 dates.** On FY15E $1.395-1.445 (and FY14E $1.545 in January), 19-25x GAAP EPS against an 18.5x median, the stock
  ($31.33-35.76) returned -0.6% to +23.8% over two years while SPY returned +13.1% to +38.8%; it lagged on every date (by 2.0-22.4pp) and
  cleared the hurdle on none. Its m12-24 average price sat 7.1% under to 6.1% over the entry. Over three years 44 of 53 held (9 beat SPY,
  none cleared the hurdle).
- **Entry price ranks the outcome** at -0.97 (m12-24) and -0.74 (two years); the EPP gap at -0.81 and -0.68, the right sign.
- **The two-year price landed nearest BULL on all 53 dates**, as the BULL case (the history's EPS CAGR, -0.1% to +3.7%/yr) sat close to
  the entry price.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST | 3 | +13.2% | +11.9% to +14.7% | 0 | 0 | +4.8% | 0 |
| class RICH, legacy tier AVOID | 49 | +28.8% | +8.6% to +54.5% | 18 | 13 | +11.0% | 31 |
| FY15E $1.40 (2016-01-08 to 2016-01-29) | 4 | +28.3% | +25.6% to +36.1% | 1 | 0 | +11.7% | 3 |
| FY16E $1.605 (2016-02-03 to 2016-04-29) | 13 | +26.6% | +16.0% to +33.4% | 1 | 0 | +15.7% | 12 |
| FY16E $1.785 (2016-05-04 to 2016-07-29) | 13 | +11.2% | +8.6% to +15.0% | 0 | 0 | +1.6% | 10 |
| FY16E $1.11 (2016-08-03 to 2016-12-30) | 22 | +41.4% | +22.2% to +54.5% | 16 | 13 | +17.1% | 6 |
| latest print Q3 2015 (2016-01-08 to 2016-01-29) | 4 | +28.3% | +25.6% to +36.1% | 1 | 0 | +11.7% | 3 |
| latest print Q4 2015 (2016-02-03 to 2016-04-29) | 13 | +26.6% | +16.0% to +33.4% | 1 | 0 | +15.7% | 12 |
| latest print Q1 2016 (2016-05-04 to 2016-07-29) | 13 | +11.2% | +8.6% to +15.0% | 0 | 0 | +1.6% | 10 |
| latest print Q2 2016 (2016-08-03 to 2016-10-28) | 13 | +34.2% | +22.2% to +46.4% | 7 | 4 | +8.1% | 6 |
| latest print Q3 2016 (2016-11-02 to 2016-12-30) | 9 | +44.5% | +37.2% to +54.5% | 9 | 9 | +21.3% | 0 |

- **RICH held on 31 of 49; the 3 FAIR dates failed.** From January to July 2016, on FY15E $1.40 and FY16E $1.605 and $1.785, RICH held
  on 25 of 27 (+8.6% to +36.1% against SPY's stronger run); the three FAIR dates of May 2016 ($33.19-34.61) returned +11.9% to +14.7% and
  lagged SPY by 22.5-23.4pp, so FAIR's ±15pp band failed where RICH would have held.
- **The RICH calls on FY15's $1.11 failed.** From 2016-08-03, with no reported EPS guide in force, the stock was 27.6-31.8x the last GAAP
  year and RICH: the 22 dates ($30.63-35.29) returned +22.2% to +54.5% over two years (to late 2018), cleared the hurdle on 16 and beat
  SPY on 13; 6 held. Over three years 39 of the year's 52 dates held and 9 cleared the hurdle.
- **The signals and gaps ranked with the wrong signs**: the proxy composite at -0.75 against the two-year return, Ratio B at +0.68, the
  EPP gap at +0.45, because the highest-multiple dates (the $1.11 dates) were the ones that rose most. Entry price ranks the m12-24
  average price at -0.82.
- **The two-year price landed nearest BULL on 19 dates, XBULL on 19 and BASE on 14.**

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +31.0% | +7.0% to +43.9% | 21 | 29 | +20.9% | 23 |
| FY16E $1.11 (2017-01-06 to 2017-01-27) | 4 | +40.0% | +36.3% to +42.2% | 4 | 4 | +24.2% | 0 |
| FY17E $1.17 (2017-02-01 to 2017-12-29) | 48 | +27.7% | +7.0% to +43.9% | 17 | 25 | +20.7% | 23 |
| latest print Q3 2016 (2017-01-06 to 2017-01-27) | 4 | +40.0% | +36.3% to +42.2% | 4 | 4 | +24.2% | 0 |
| latest print Q4 2016 (2017-02-01 to 2017-04-28) | 13 | +32.0% | +25.0% to +43.9% | 6 | 11 | +19.1% | 2 |
| latest print Q1 2017 (2017-05-03 to 2017-07-28) | 13 | +36.1% | +31.6% to +39.9% | 11 | 13 | +26.8% | 0 |
| latest print Q2 2017 (2017-08-02 to 2017-10-27) | 13 | +11.1% | +7.0% to +23.8% | 0 | 1 | +18.3% | 12 |
| latest print Q3 2017 (2017-11-01 to 2017-12-29) | 9 | +15.0% | +10.6% to +16.7% | 0 | 0 | +12.5% | 9 |

- **RICH held on 23 of 52 at two years and on all 52 at three.** The four January dates (still on FY15's $1.11) and the 26 from the Q4
  2016 print to 2017-07-28 (on FY16's $1.17, 27-31x) returned +25.0% to +43.9% to early and mid 2019, cleared the hurdle on 21 and beat
  SPY on 28: 2 held. The 22 dates from the Q2 2017 print ($32.67-37.20) returned +7.0% to +23.8% and held on 21. Over three years (to
  the end of 2020) every 2017 date lagged SPY (-0.5% to +40.8% against stronger benchmark returns) and none cleared the hurdle.
- **Ratio B was infinite on every 2017 date** (the price above the BULL price), so it ranks nothing; the EPP gap ranks the m12-24 average
  price at -0.93 and the two-year return at -0.69, entry price at -0.89 and -0.78.
- **The two-year price landed nearest BULL on 42 dates and XBULL on 10.**

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 48 | +0.8% | -11.7% to +19.7% | 0 | 6 | -2.4% | 6 |
| class RICH, legacy tier AVOID | 4 | +15.7% | +9.3% to +17.2% | 0 | 0 | +8.3% | 4 |
| FY17E $1.17 (2018-01-05 to 2018-01-26) | 4 | +15.7% | +9.3% to +17.2% | 0 | 0 | +8.3% | 4 |
| FY18E $3.52 (2018-01-31 to 2018-12-28) | 48 | +0.8% | -11.7% to +19.7% | 0 | 6 | -2.4% | 6 |
| latest print Q3 2017 (2018-01-05 to 2018-01-26) | 4 | +15.7% | +9.3% to +17.2% | 0 | 0 | +8.3% | 4 |
| latest print Q4 2017 (2018-01-31 to 2018-04-27) | 13 | +6.3% | -10.2% to +19.7% | 0 | 2 | +8.4% | 2 |
| latest print Q1 2018 (2018-05-02 to 2018-07-27) | 13 | +5.5% | -2.1% to +16.0% | 0 | 4 | +2.3% | 4 |
| latest print Q2 2018 (2018-08-01 to 2018-10-26) | 13 | -6.9% | -11.7% to +3.7% | 0 | 0 | -14.0% | 0 |
| latest print Q3 2018 (2018-10-31 to 2018-12-28) | 9 | -3.9% | -10.8% to +5.7% | 0 | 0 | -15.9% | 0 |

- **CHEAP held on 6 of 48: the multiple was read on a tax-inflated year.** With no reported guide, FY18E was FY17's $3.52, which carries the
  $10.7 billion Tax Act benefit, so the stock ($34.16-46.23) read 10-13x and CHEAP all year. It returned -11.7% to +19.7% over two years
  (median +0.8%), cleared the hurdle on no date and beat SPY on 6 (March-May 2018, by 0.1-4.4pp); the two-year price landed nearest BEAR
  on all 48. Over three years (into the 2021 vaccine run) 6 held and 2 cleared the hurdle; none beat SPY.
- **January 2018's RICH dates held** (4 of 4): on FY16's $1.17, 31-33x, they returned +9.3% to +17.2% and lagged SPY.
- **Entry price ranks the outcome** at -0.94 against the m12-24 average price; the EPP gap at -0.69, Ratio B at -0.68.
- **Hindsight on the near case:** with 2017 excluded on the Tax Act benefit alone (the README sensitivity), the 48 CHEAP dates read RICH
  on FY16's $1.17, and 42 of them would have held where 6 CHEAP calls did. Hypothesis, not a rule: a one-time tax benefit standing in
  as current-year EPS may mislead the multiple; test the benefit-only reading of the r2 mirror test on other tickers' Tax Act years,
  never re-encode PFE.

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 4 | -0.3% | -2.9% to +4.0% | 0 | 0 | -13.5% | 0 |
| class RICH, legacy tier AVOID | 48 | +10.7% | -11.2% to +72.0% | 18 | 6 | -6.2% | 30 |
| FY18E $3.52 (2019-01-04 to 2019-01-25) | 4 | -0.3% | -2.9% to +4.0% | 0 | 0 | -13.5% | 0 |
| FY19E $1.86 (2019-01-30 to 2019-12-27) | 48 | +10.7% | -11.2% to +72.0% | 18 | 6 | -6.2% | 30 |
| latest print Q3 2018 (2019-01-04 to 2019-01-25) | 4 | -0.3% | -2.9% to +4.0% | 0 | 0 | -13.5% | 0 |
| latest print Q4 2018 (2019-01-30 to 2019-04-26) | 13 | -3.5% | -11.2% to +10.9% | 0 | 0 | -11.7% | 13 |
| latest print Q1 2019 (2019-05-01 to 2019-07-26) | 13 | +6.1% | +2.2% to +10.7% | 0 | 0 | -9.6% | 13 |
| latest print Q2 2019 (2019-07-30 to 2019-10-25) | 13 | +35.5% | +25.3% to +62.3% | 10 | 1 | +12.8% | 3 |
| latest print Q3 2019 (2019-10-30 to 2019-12-27) | 9 | +50.0% | +27.9% to +72.0% | 8 | 5 | +12.1% | 1 |

- **RICH held on 30 of 48; the January CHEAP dates failed** (4 of 4, still on FY17's $3.52, -2.9% to +4.0%). On FY18's $1.86 (18.5-23.6x)
  the 26 dates to 2019-07-26 returned -11.2% to +10.9% over two years against SPY's +42.5% or more and all held; the 22 from the Q2 2019
  print ($34.34-39.32, after the Upjohn-Mylan announcement) returned +25.3% to +72.0% into 2021, cleared the hurdle on 18 and held on 4.
  Over three years 22 held and 26 beat SPY.
- **Entry price ranks the outcome** at -0.90 (m12-24) and -0.79 (two years); the EPP gap at -0.59 and -0.54, the proxy composite at -0.74
  and -0.69 (wrong signs: its 2019 readings fell as revenues fell, before the rise).

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 2 | +34.0% | +33.5% to +34.0% | 2 | 2 | +24.5% | 2 |
| class CHEAP, legacy tier BUY | 47 | +48.9% | +27.7% to +109.1% | 45 | 44 | +39.0% | 47 |
| class RICH, legacy tier AVOID | 4 | +58.1% | +44.4% to +61.5% | 4 | 4 | +14.3% | 0 |
| FY19E $1.86 (2020-01-03 to 2020-01-24) | 4 | +58.1% | +44.4% to +61.5% | 4 | 4 | +14.3% | 0 |
| FY20E $2.87 (2020-01-29 to 2020-12-31) | 49 | +47.9% | +27.7% to +109.1% | 47 | 46 | +38.9% | 49 |
| latest print Q3 2019 (2020-01-03 to 2020-01-24) | 4 | +58.1% | +44.4% to +61.5% | 4 | 4 | +14.3% | 0 |
| latest print Q4 2019 (2020-01-29 to 2020-04-24) | 13 | +60.4% | +44.3% to +109.1% | 13 | 11 | +35.3% | 13 |
| latest print Q1 2020 (2020-04-29 to 2020-07-24) | 13 | +57.3% | +44.1% to +79.8% | 13 | 12 | +41.6% | 13 |
| latest print Q2 2020 (2020-07-29 to 2020-10-23) | 13 | +41.4% | +27.7% to +48.9% | 11 | 13 | +39.7% | 13 |
| latest print Q3 2020 (2020-10-28 to 2020-12-31) | 10 | +44.8% | +33.5% to +50.3% | 10 | 10 | +35.5% | 10 |

- **CHEAP held on all 49 dates; the January RICH dates failed.** On FY19's $2.87 (10-14x; the joint-venture gain and Upjohn inside, and
  from 2020-11-20 a price without Viatris), the stock ($29.01-41.12, the COVID low of March included) returned +27.7% to +109.1% over two
  years into the vaccine run of 2021-2022, cleared the hurdle on 47 and beat SPY on 46. The four January dates on FY18's $1.86 (21-22x,
  RICH) returned +44.4% to +61.5% and failed. Over three years (to 2023, after the peak) 7 of 53 held, 2 cleared the hurdle.
- **Entry price ranks the m12-24 average price at -0.76**; the EPP gap at -0.71, Ratio B at -0.81. The two-year price landed nearest
  BASE on 49 dates.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 3 | +12.2% | +8.8% to +15.0% | 0 | 3 | +21.7% | 3 |
| class CHEAP, legacy tier BUY | 46 | +0.1% | -40.8% to +45.7% | 6 | 20 | +12.4% | 20 |
| class FAIR, legacy tier BUY | 3 | -46.1% | -49.8% to -45.8% | 0 | 0 | -36.6% | 0 |
| FY20E $2.87 (2021-01-08 to 2021-01-29) | 4 | +39.0% | +30.8% to +45.7% | 2 | 4 | +35.2% | 4 |
| FY21E $1.24 (2021-02-03 to 2021-12-31) | 48 | -2.2% | -49.8% to +35.6% | 4 | 19 | +9.3% | 19 |
| latest print Q3 2020 (2021-01-08 to 2021-01-29) | 4 | +39.0% | +30.8% to +45.7% | 2 | 4 | +35.2% | 4 |
| latest print Q4 2020 (2021-02-03 to 2021-04-30) | 13 | +21.8% | +8.8% to +35.6% | 4 | 13 | +35.5% | 13 |
| latest print Q1 2021 (2021-05-05 to 2021-07-23) | 12 | +4.3% | -2.6% to +11.5% | 0 | 6 | +15.5% | 6 |
| latest print Q2 2021 (2021-07-29 to 2021-10-29) | 14 | -15.2% | -23.8% to -8.2% | 0 | 0 | -5.4% | 0 |
| latest print Q3 2021 (2021-11-03 to 2021-12-31) | 9 | -39.3% | -49.8% to -23.1% | 0 | 0 | -27.6% | 0 |

- **CHEAP held on 23 of 49, FAIR failed on 3, and none held at three years.** The four January dates (FY20E $2.87) and the 13 from the Q4
  2020 print to April ($33.49-38.66) returned +8.8% to +45.7% over two years and held; from the Q1 2021 print the price rose to $59.48 while
  FY21E stayed at FY20's $1.24 and BASE took the vaccine revenue ranges (+73% to +97%/yr): those 35 dates (32 CHEAP, 3 FAIR) returned -49.8% to +11.5% to
  2023, 6 held, and the three FAIR dates of late December ($58.71-59.48) lost 45.8-49.8%. Over three years every 2021 date lost (-47.3% to
  -4.4%) and lagged SPY.
- **Rankings:** entry price ranks the m12-24 average price at -0.99 and the two-year return at -0.96; Ratio B ranks them at +0.69 and
  +0.71, the wrong sign, as the vaccine BASE lowered Ratio B most where the price was highest. The two-year price landed nearest BEAR on
  35 dates and BASE on 17.
- **Hypothesis, not a rule:** a revenue guide lifted by one product's temporary surge, read as two years of EPS growth, may overstate
  BASE; test a guide-level check (one product's share of the guided growth) on other tickers and periods, never fit to PFE.

## The encoding calls, seen afterwards (2008-2009)

Only one judgement call recorded in retro/README.md ("PFE") moves classes: the 2003 exclusion taking the history and the window with it.
Read as only 2003 leaving (a ten-year window), the three January 2008 dates are CHEAP instead of RICH, and by the two-year test they
would have held (each beat SPY) where the RICH call failed; no other date moves. Every signal at its BEAR value moves 2009-10-16 from
CHEAP to RICH (a +15.5% return that lagged SPY by 1.4pp, which RICH would have called). GAAP or adjusted EPS, 2008 kept or excluded,
the revenue guides used or not and the dividend's timing move no class. Across all 105 dates the call held on 69 (30 + 0 in 2008, 39 in
2009); what decided the outcomes was where the stock entered the crash, as with every one-stock series, and the floor that method r2
takes from a window whose multiples were falling. Both are hypotheses to test across tickers, never a reason to re-encode PFE.

## The encoding calls, seen afterwards (2010-2013)

The calls of 2010-2013 held on 100 of 209 dates at two years (47, 4, 16 and 33 a year) and 95 at three. Scored against the same
outcomes, the README's sensitivity variants would have held on: the company's adjusted EPS throughout 142 (49 gained in 2011-2013, 7
lost in the second half of 2013); the Zoetis gain out of the 2013 guides 109 (16 gained, 7 lost); the dollar revenue guides unused 109;
only 2003 leaving 111; every signal at XBULL 108; the FY2010 guides on the pro forma Wyeth year 68 (32 lost in 2010-2011). 2008 excluded,
the restated years ignored and the ex-divestiture ranges on a base without the business move no class or no held call. What separated
the outcomes was the EPS line the multiple was read on (GAAP with recurring amortization and one-time gains, against an adjusted
figure), and the stock's rerating from the bottom of its own 2004-2011 range while reported EPS fell, which the BULL case, built on a
negative history CAGR, did not reach. Both are hypotheses to test across tickers, never a reason to re-encode PFE: the encodings were
decided before any outcome existed, and changing one means a new method version and a full re-run.

## The encoding calls, seen afterwards (2014-2017)

The calls of 2014-2017 held on 127 of 209 dates at two years (20, 53, 31 and 23 a year) and 180 at three. Scored against the same
outcomes, the README's sensitivity variants would have held on: the adjusted EPS guide as current-year EPS where no reported guide was in
force 155 (57 gained: 12 in 2014, 16 in 2016, 29 in 2017; 29 lost: 6 in 2016, 23 in 2017); the Q2 2016 policy not read as a withdrawal
133 (6 gained); the history from 2004 in every vintage, the FY2016 ranges on pro forma 2015 revenues and every signal at BEAR 130 each (3
gained, the May 2016 FAIR dates); every signal at XBULL 124 (3 lost); the dollar revenue guides unused 114 (1 gained, 14 lost in 2016).
The Q1 2014 withdrawal and the 2016-02-16 reissue move no class.

What separated the outcomes was again the EPS line the multiple was read on. GAAP EPS carried $0.40-0.48 a share of recurring
amortization every year, and once Pfizer stopped guiding GAAP EPS (from 2016-08-02) the last GAAP year stood as current-year EPS, so the
stock read 27-32x and RICH while it rose 22-54% over two years from August 2016 to July 2017; the GAAP reading held in the flat 2015
and in the second half of 2017. Hypotheses to test across tickers, never a reason to re-encode PFE: a company that guides only
non-GAAP EPS may need a current-year EPS other than the last GAAP year when its GAAP figure carries large recurring amortization; and,
as in every one-stock series, entry price ranks the outcome (-0.82 to -0.97 against the m12-24 average price each year). The encodings
were decided before any outcome existed, and changing one means a new method version and a full re-run.

## The encoding calls, seen afterwards (2018-2021)

The calls of 2018-2021 held on 112 of 209 dates at two years (10, 30, 49 and 23 a year) and 35 at three. Scored against the same outcomes,
the README's sensitivity variants would have held on: 2017 excluded on the Tax Act benefit alone 154 (48 gained, 6 lost); every signal at
BEAR 116 (7 gained, 3 lost); the adjusted EPS guide as current-year EPS 104 (22 gained, 30 lost); the dollar revenue guides unused 99 (13
lost in early 2021); the restated 2016 loss as a gap, Yahoo's distribution factor kept, the Q4 2020 restatement ignored and every signal
at XBULL 112 each. What separated the outcomes was, again, the GAAP year that stood in for current-year EPS with no reported guide: the
tax-inflated 2017 made 2018 look cheap and was wrong, the gain-inflated 2019 (with Upjohn) made 2020 look cheap and was right, and in 2021
a revenue guide driven by one product carried BASE. These are hypotheses to test across tickers, never a reason to re-encode PFE: the
encodings were decided before any outcome existed, and changing one means a new method version and a full re-run.
