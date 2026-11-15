# SO retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SO weekly dates: 314 from 2008-01-04 to 2013-12-31, all The Southern Company (NYSE: SO). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build
and README were committed: 2008-2009 (db1a562, fe0a6be) and 2010-2013 (bcf8478, fa842e0, with the firewall result); both were scored on
2026-11-15. While reading the FY2009 10-K for 2010-2013 the builder found that the FY2008 10-K already gave the company's EPS excluding
only the leveraged lease charges ($2.37); under the rule decided for 2008-2009 that is FY2008's figure from 2009-02-25, so the 45 dates from
2009-02-27 were rebuilt and re-scored (3 classes moved, all toward calls that held: retro/README.md, "SO 2010-2013"). The 2009 figures below
are the corrected ones. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2016-12-30). Total returns include the
quarterly dividends ($0.4025 from the ex-date of 2008-01-31, $0.42 from 2008-05-01, $0.4375 from 2009-04-30, $0.455 from 2010-04-29,
$0.4725 from 2011-04-28, $0.49 from 2012-05-03, $0.5075 from 2013-05-02, $0.525 from 2014-05-01, $0.5425 from 2015-05-14, $0.56 from
2016-05-12): $3.12-4.24 a share over two years, 7.7-13.2% of the entry price. No split or distribution falls in any horizon, so every price
is as traded. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years
and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within
±15pp of the benchmark, and RICH should miss the hurdle and lag the benchmark. A year's table runs to the last date of the calendar year;
2009-01-02 closes the ISO week of 2008-12-29 and sits in the 2009 table.

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 15 | +7.7% | +1.9% to +27.7% | 0 | 12 | -7.1% | 12 |
| class CHEAP, legacy tier ACCUMULATE | 5 | +3.0% | -0.1% to +9.4% | 0 | 5 | -10.5% | 5 |
| class FAIR, legacy tier ACCUMULATE | 5 | +5.1% | +3.0% to +7.9% | 0 | 5 | -11.7% | 0 |
| class RICH, legacy tier BUY | 11 | +15.6% | -3.3% to +20.8% | 0 | 3 | -2.8% | 8 |
| class RICH, legacy tier ACCUMULATE | 9 | +2.9% | -2.6% to +12.9% | 0 | 8 | -12.6% | 1 |
| class RICH, legacy tier WATCHLIST | 4 | +2.9% | +0.3% to +6.1% | 0 | 4 | -13.4% | 0 |
| class RICH, legacy tier AVOID | 3 | -5.3% | -7.8% to -2.7% | 0 | 3 | -19.0% | 0 |
| FY07E = FY06's $2.10 (2008-01-04 to 2008-01-25) | 4 | -2.7% | -7.8% to +0.3% | 0 | 4 | -17.2% | 0 |
| FY08E = FY07's $2.29 (Q4 2007 release) (2008-01-31 to 2008-02-22) | 4 | -2.6% | -3.3% to +0.7% | 0 | 4 | -12.8% | 0 |
| FY08E = FY07's $2.28 (FY2007 10-K) (2008-02-29 to 2008-12-26) | 44 | +6.5% | -0.1% to +27.7% | 0 | 32 | -8.9% | 26 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -2.7% | -7.8% to +0.3% | 0 | 4 | -17.2% | 0 |
| latest print Q4 2007 (2008-01-31 to 2008-04-25) | 13 | +1.3% | -3.3% to +4.2% | 0 | 13 | -12.9% | 3 |
| latest print Q1 2008 (2008-05-01 to 2008-07-25) | 13 | +4.0% | -0.1% to +12.0% | 0 | 13 | -7.7% | 10 |
| latest print Q2 2008 (2008-07-31 to 2008-10-17) | 12 | +7.9% | +3.9% to +27.7% | 0 | 10 | -10.1% | 4 |
| latest print Q3 2008 (2008-10-24 to 2008-12-26) | 10 | +16.9% | +12.9% to +20.8% | 0 | 0 | -2.4% | 9 |

- **CHEAP held on 17 of its 20 dates, by beating a falling SPY, never by the hurdle.** The CHEAP dates of 2008 ($32.26-37.15, 14.1-16.3x
  FY07's $2.28) returned -0.1% to +27.7% over two years, dividends included, while SPY returned -18.7% to +36.8%; 17 beat it, none cleared
  the 32.2% hurdle, and the return to the m12-24 average price was -11.9% to +5.0%. The three misses are the CHEAP dates of October 2008
  after the crash (2008-10-10, 2008-10-17, 2008-10-31: +20.6% to +27.7%, 6-9pp behind SPY's rebound from its March 2009 low).
- **The RICH calls of January and February 2008 missed on all eight, though the stock fell.** On FY06's $2.10 (17.2-18.9x, AVOID on three)
  and then on the Q4 2007 print (15.5-15.9x), the eight dates returned -7.8% to +0.7% over two years and their m12-24 average price was
  12-21% under the entry, but SPY fell 10-18%, so each beat it by 7-16pp and the call (miss the hurdle and lag the benchmark) missed. Over
  three years they returned +8.2% to +21.5%, 12-19pp ahead of SPY. Every one sat through a 32-34% drawdown to the 2009-03-12 low ($26.81).
- **The other RICH dates of 2008 held on 9 of 19, FAIR on none of 5.** The RICH calls held where SPY's 2009-2010 rebound outran SO (the
  dates of late October to December 2008) and missed where SO beat a falling SPY (March-April and August-September 2008, +0.9% to +6.5%);
  the five FAIR dates returned +3.0% to +7.9% and beat SPY by 15-21pp, outside the ±15pp band. After two years the 2008 dates landed at the
  BEAR (28) or BASE (24) scenario price.
- **The anchor lagged and the multiple was set by Mirant.** Both the four January dates on FY06's $2.10 (FY07 came in at $2.28) and the
  14x floor ($29.40-32.06, from yearly lows that include 1998-1999 at 16.6-17.1x with Mirant in the price) proved too high for the 2009
  low ($26.81, 11.3x FY08's $2.37 and 11.9x its GAAP $2.25). Hypothesis, not a rule: a window that spans a large spin-off and keeps the pre-spin prices sets the
  floor and the median too high; test it on other tickers with spin-offs inside the window (BMY's started after Zimmer), never fit it to SO.

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 15 | +37.4% | +20.8% to +59.1% | 13 | 2 | +18.9% | 13 |
| class FAIR, legacy tier BUY | 1 | +52.8% | +52.8% | 1 | 1 | +31.1% | 1 |
| class RICH, legacy tier BUY | 36 | +43.0% | +17.1% to +50.8% | 33 | 25 | +22.1% | 3 |
| class RICH, legacy tier ACCUMULATE | 1 | +11.5% | +11.5% | 0 | 0 | -6.2% | 1 |
| FY08E = FY07's $2.28 (FY2007 10-K) (2009-01-02 to 2009-01-23) | 4 | +20.0% | +11.5% to +20.6% | 0 | 0 | +0.9% | 4 |
| FY09E = FY08's $2.26 (Q4 2008 release) (2009-01-29 to 2009-02-20) | 4 | +32.5% | +20.8% to +37.4% | 2 | 0 | +13.9% | 2 |
| FY09E = FY08's $2.37 (the company's, excluding the leveraged lease charges; FY2008 10-K) (2009-02-27 to 2009-12-31) | 45 | +43.0% | +32.7% to +59.1% | 45 | 28 | +22.1% | 12 |
| latest print Q3 2008 (2009-01-02 to 2009-01-23) | 4 | +20.0% | +11.5% to +20.6% | 0 | 0 | +0.9% | 4 |
| latest print Q4 2008 (2009-01-29 to 2009-04-24) | 13 | +35.9% | +20.8% to +54.2% | 11 | 0 | +18.7% | 11 |
| latest print Q1 2009 (2009-04-30 to 2009-07-24) | 13 | +43.1% | +34.9% to +59.1% | 13 | 6 | +23.7% | 3 |
| latest print Q2 2009 (2009-07-30 to 2009-10-23) | 13 | +42.6% | +35.6% to +45.6% | 13 | 12 | +21.9% | 0 |
| latest print Q3 2009 (2009-10-29 to 2009-12-31) | 10 | +48.2% | +41.0% to +50.8% | 10 | 10 | +24.2% | 0 |

- **The January 2009 RICH calls held** (2009-01-02 to 2009-01-23, the Q3 2008 print, $34.65-37.47): +11.5% to +20.6% over two years,
  29-39pp behind SPY's rebound, under the hurdle.
- **CHEAP from the Q4 2008 print to 2009-04-24 held on 11 of 13, all by the hurdle.** At $27.14-33.86 (12.1-15.0x, the 0th-32nd percentile)
  the 13 dates returned +20.8% to +54.2% over two years; 11 cleared the hurdle, none kept up with SPY's +55.9% to +98.7% from its lows. The
  two misses are the first two (2009-01-29 and 2009-02-06: +20.8% and +21.8%). Over three years they returned +47.7% to +87.5%.
- **From the Q1 2009 print the class missed on 33 of 36 dates while the tier said BUY.** At $27.70-34.22 (11.7-14.4x the corrected $2.37,
  the 0th-45th percentile; the price under the BEAR case on 27) the 36 dates returned +34.9% to +59.1% over two years, dividends
  included: every one over the hurdle and 28 ahead of SPY; over three years +43.8% to +84.4%, all 36 ahead of SPY by 8-35pp and 31 over
  the three-year hurdle; the largest drawdown inside two years was 9%. 33 were RICH and missed (the adjusted gap: a proxy composite of
  1.30-1.95 reading the recession in the quarter's retail kWh, segment earnings and revenue, BASE negative with revenue as reported); the
  corrected anchor moved 2009-05-15 and 2009-05-22 to CHEAP and 2009-05-29 to FAIR, and those three held. After two years the 36 dates
  landed at the BULL (31) or BASE (5) scenario price.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 20 | +51.0% | +42.2% to +55.0% | 20 | 20 | +28.4% | 20 |
| class RICH, legacy tier BUY | 10 | +45.7% | +41.9% to +50.5% | 10 | 10 | +25.1% | 0 |
| class RICH, legacy tier ACCUMULATE | 13 | +25.5% | +20.7% to +42.6% | 3 | 12 | +19.9% | 1 |
| class RICH, legacy tier WATCHLIST | 5 | +33.2% | +31.4% to +34.7% | 4 | 2 | +21.5% | 1 |
| class RICH, legacy tier AVOID | 4 | +32.2% | +31.2% to +32.3% | 2 | 4 | +20.3% | 0 |
| FY09E = FY08's $2.37 (the company's, excluding the leveraged lease charges) (2010-01-08 to 2010-01-22) | 3 | +46.8% | +46.7% to +50.5% | 3 | 3 | +23.5% | 0 |
| FY10E = FY09's $2.32 (the company's, excluding the MC Asset Recovery settlement) (2010-01-28 to 2010-12-31) | 49 | +42.7% | +20.7% to +55.0% | 36 | 45 | +24.5% | 22 |
| latest print Q3 2009 (2010-01-08 to 2010-01-22) | 3 | +46.8% | +46.7% to +50.5% | 3 | 3 | +23.5% | 0 |
| latest print Q4 2009 (2010-01-28 to 2010-04-23) | 13 | +48.7% | +41.9% to +55.0% | 13 | 13 | +28.0% | 7 |
| latest print Q1 2010 (2010-04-29 to 2010-07-23) | 13 | +47.6% | +42.2% to +55.0% | 13 | 13 | +27.5% | 13 |
| latest print Q2 2010 (2010-07-29 to 2010-10-22) | 13 | +33.2% | +31.2% to +45.7% | 10 | 10 | +21.5% | 1 |
| latest print Q3 2010 (2010-10-28 to 2010-12-31) | 10 | +23.3% | +20.7% to +31.3% | 0 | 9 | +19.5% | 1 |

- **The CHEAP calls of the first half held on all 20.** On FY09's $2.32 (the company's figure excluding the MC Asset Recovery settlement)
  at $31.17-35.89 (13.4-15.5x), the 20 CHEAP dates returned +42.2% to +55.0% over two years, every one over the hurdle and 12.6-30.4pp ahead of
  SPY. The six RICH dates among them (2010-03-19 to 2010-04-23, on BASE -9.9%/yr from Q4 2009 revenue) and the three of January 2010 (BASE
  -15.0%/yr) returned +41.9% to +50.5% and missed.
- **From the Q2 2010 print RICH missed on 37 of its first 39 dates** (2010-07-29 to 2011-04-21, $35.49-38.56, 15.3-16.6x and the 57th-92nd
  percentile): +20.7% to +45.7% over two years, 35 of them ahead of SPY and 14 over the hurdle. Over three years they fell behind: +21.7% to
  +42.8%, 13-36pp behind SPY on every one.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier ACCUMULATE | 3 | +23.7% | +21.7% to +24.0% | 0 | 3 | +18.3% | 0 |
| class RICH, legacy tier WATCHLIST | 5 | +28.7% | +26.6% to +32.9% | 1 | 5 | +20.4% | 0 |
| class RICH, legacy tier AVOID | 44 | +18.8% | -2.9% to +35.8% | 3 | 10 | +12.4% | 34 |
| FY10E = FY09's $2.32 (the company's, excluding the MC Asset Recovery settlement) (2011-01-07 to 2011-01-21) | 3 | +23.7% | +21.7% to +24.0% | 0 | 3 | +18.3% | 0 |
| FY11E = FY10's $2.37 (Q4 2010 release) (2011-01-27 to 2011-02-18) | 4 | +26.6% | +26.0% to +27.6% | 0 | 4 | +19.3% | 0 |
| FY11E = FY10's $2.36 (FY2010 10-K) (2011-02-25 to 2011-12-30) | 45 | +18.8% | -2.9% to +35.8% | 4 | 11 | +12.4% | 34 |
| latest print Q3 2010 (2011-01-07 to 2011-01-21) | 3 | +23.7% | +21.7% to +24.0% | 0 | 3 | +18.3% | 0 |
| latest print Q4 2010 (2011-01-27 to 2011-04-21) | 13 | +28.7% | +26.0% to +35.8% | 4 | 13 | +18.8% | 0 |
| latest print Q1 2011 (2011-04-28 to 2011-07-22) | 13 | +22.8% | +17.1% to +32.1% | 0 | 2 | +14.1% | 11 |
| latest print Q2 2011 (2011-07-28 to 2011-10-21) | 13 | +10.6% | +4.0% to +22.6% | 0 | 0 | +8.8% | 13 |
| latest print Q3 2011 (2011-10-27 to 2011-12-30) | 10 | +3.4% | -2.9% to +7.1% | 0 | 0 | +0.3% | 10 |

- **RICH held on 34 of 52: on none of the 16 dates to 2011-04-21 and on 34 of the 36 after.** The dates to 2011-04-21 (15.7-16.6x, the
  69th-92nd percentile) returned +21.7% to +35.8% over two years, 3.7-15.2pp ahead of SPY, and missed. From the Q1 2011 print (2011-04-28,
  $38.85-46.29, 16.5-19.6x, the 92nd-100th percentile, Ratio B infinite from 2011-09-16) the 36 dates returned -2.9% to +32.1%; 34 missed the
  hurdle and lagged SPY (+20.5% to +60.6%) and held, the first two (2011-04-28 and 2011-05-06) beat it and missed.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +4.8% | -0.9% to +28.9% | 0 | 0 | -5.5% | 52 |
| FY11E = FY10's $2.36 (FY2010 10-K) (2012-01-06 to 2012-01-20) | 3 | -0.3% | -0.4% to -0.1% | 0 | 0 | -3.7% | 3 |
| FY12E = FY11's $2.57 (Q4 2011 release) (2012-01-26 to 2012-02-24) | 5 | +2.1% | -0.3% to +4.8% | 0 | 0 | -2.7% | 5 |
| FY12E = FY11's $2.55 (FY2011 10-K) (2012-03-02 to 2012-12-28) | 44 | +6.0% | -0.9% to +28.9% | 0 | 0 | -6.2% | 44 |
| latest print Q3 2011 (2012-01-06 to 2012-01-20) | 3 | -0.3% | -0.4% to -0.1% | 0 | 0 | -3.7% | 3 |
| latest print Q4 2011 (2012-01-26 to 2012-04-20) | 13 | +4.8% | -0.3% to +8.5% | 0 | 0 | -2.7% | 13 |
| latest print Q1 2012 (2012-04-26 to 2012-07-20) | 13 | +3.7% | -0.9% to +9.5% | 0 | 0 | -8.0% | 13 |
| latest print Q2 2012 (2012-07-26 to 2012-11-02) | 15 | +5.3% | +0.1% to +11.1% | 0 | 0 | -7.0% | 15 |
| latest print Q3 2012 (2012-11-06 to 2012-12-28) | 8 | +21.1% | +15.8% to +28.9% | 0 | 0 | +1.8% | 8 |

- **RICH held on all 52** ($42.03-48.08, 16.5-19.2x on FY10's $2.36 to the Q4 2011 print, then FY11's $2.57 and $2.55, the 81st-100th
  percentile; Ratio B infinite on most): two-year returns of -0.9% to +28.9%, every one under the hurdle and 25-52pp behind SPY's +34% to +56%.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY | 3 | +20.2% | +20.1% to +21.2% | 0 | 3 | +12.0% | 0 |
| class RICH, legacy tier ACCUMULATE | 12 | +18.4% | +12.3% to +25.6% | 0 | 3 | +10.3% | 9 |
| class RICH, legacy tier WATCHLIST | 10 | +14.0% | +4.4% to +20.2% | 0 | 0 | +7.2% | 10 |
| class RICH, legacy tier AVOID | 28 | +5.6% | -0.6% to +27.5% | 0 | 0 | +1.1% | 28 |
| FY12E = FY11's $2.55 (FY2011 10-K) (2013-01-04 to 2013-01-25) | 4 | +26.7% | +21.1% to +27.5% | 0 | 0 | +2.9% | 4 |
| FY13E = FY12's $2.68 (the company's, excluding the insurance gain) (2013-01-31 to 2013-12-31) | 49 | +12.3% | -0.6% to +25.6% | 0 | 6 | +3.7% | 43 |
| latest print Q3 2012 (2013-01-04 to 2013-01-25) | 4 | +26.7% | +21.1% to +27.5% | 0 | 0 | +2.9% | 4 |
| latest print Q4 2012 (2013-01-31 to 2013-04-19) | 12 | +7.5% | -0.6% to +22.8% | 0 | 0 | +0.7% | 12 |
| latest print Q1 2013 (2013-04-25 to 2013-07-26) | 14 | +4.6% | +1.9% to +9.1% | 0 | 0 | +1.2% | 14 |
| latest print Q2 2013 (2013-08-01 to 2013-10-25) | 13 | +17.2% | +9.1% to +20.2% | 0 | 1 | +9.0% | 12 |
| latest print Q3 2013 (2013-10-31 to 2013-12-31) | 10 | +20.1% | +13.6% to +25.6% | 0 | 5 | +10.3% | 5 |

- **RICH held on 47 of 53.** The 16 dates to 2013-04-19 (16.4-18.1x FY11's $2.55, then FY12's $2.68) held on all, -0.6% to +27.5% over two years; from the Q1 2013 print (the Kemper quarters,
  $40.12-48.09, 15.0-17.9x) the 37 dates returned +1.9% to +25.6% over two years, none over the hurdle, and held on 31: the six misses beat SPY
  over two years. Over three years 17 of the 37 beat SPY. The Kemper encoding moved no class (README); the multiple did the work.

## Across the six years

- **Calls held on 199 of 314:** CHEAP 50 of 55, FAIR 1 of 6, RICH 148 of 253. By year: 26 of 52 in 2008, 18 of 53 in 2009, 22 of 52 in 2010,
  34 of 52 in 2011, 52 of 52 in 2012 and 47 of 53 in 2013. The RICH class missed through the 2009-2010 rebound (when SO rose with the
  market from its own low) and held once the multiple sat at the top of its decade (2011-2013).
- **The price ranks the returns in every year; the signals do not.** Across the 314 dates the entry price ranks the two-year return at
  Spearman -0.71 and the return to the m12-24 average price at -0.59, Ratio B at -0.69 and -0.58, the P/E percentile at -0.65 and -0.52, the EPP
  gap at -0.61 and -0.48 (the right signs); the adjusted gap at +0.26 and +0.19, the proxy composite at -0.14 and -0.06. Within 2010-2013:
  the price -0.92 and -0.98, Ratio B -0.80 and -0.87, the adjusted gap +0.34 and +0.43 (the right sign, unlike 2008-2009), the proxy composite
  +0.17 and +0.27.
- **Ratio B infinite** (the price above the BULL case, 63 dates from 2011-09-16 to 2013-04-19): every one held RICH, returning -2.9% to +26.7%
  over two years, none over the hurdle or ahead of SPY.
- **The measured calls, read against the outcomes (hindsight; the README's sensitivities were computed before any outcome).** In
  2010-2013 GAAP EPS throughout would have moved exactly the 20 CHEAP calls of 2010, all of which held, to RICH or FAIR; Yahoo's Mirant factor
  would have moved 6 of them; the Kemper choices moved none. In 2008-2009, scored on the first build, keeping Yahoo's factor would have held
  28 calls instead of 41 and every signal at XBULL 84 (a bracket).
- **Profile drift:** the models' DURABLE, risk 2, against today's profile of DURABLE, risk 1 (`outcome.json`; label only).

Hypotheses for the live model (test them on other tickers and periods; never fold them into this archive):
- For a regulated utility the quarter's operating signals are coincident with a recession and contrarian at its trough (2008-2009); outside
  the recession they carry little either way (2010-2013). The multiple against its own decade and Ratio B carried the ranking in both.
- When the tier and the class disagree (BUY and RICH through 2009 and early 2010) the tier was right here; when both say expensive (RICH and
  AVOID, 2011-2013) both were.
- A defensive stock's CHEAP call "holds" in a falling market by beating SPY with a flat return (2008) and its RICH call misses in a rebound by
  rising with the market (2009-2010): the benchmark leg of the call rule cuts both ways for a low-beta stock.
