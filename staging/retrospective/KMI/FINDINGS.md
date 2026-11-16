# KMI retrospective findings (hindsight)

Patterns seen in `outcome.json` for the KMI weekly dates: first the 103 of 2013-01-18 to 2014-12-31, then the 210 of 2015-2018 ("2015-2018",
below), the 209 of 2019-2022 ("2019-2022", below) and the 202 of 2023-2026 ("2023-2026", below). The first part covers the 103 dates 2013-01-18 to 2014-12-31: Kinder Morgan, Inc. (NYSE: KMI, Class P common
stock), from the first date after its first full year of GAAP EPS to the year end before its first print as the combined company.
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The series was scored only after its
point-in-time build was committed and pushed (d0407fb6d; the firewall fix 3be3f9e66; README and firewall result 3f80e93e6). Outcomes were computed on
2026-11-16: every date has its 6-month, 1-, 2- and 3-year outcomes and the return to the average price over months 12-24. Total returns
include the $0.37-0.44 quarterly dividends and the later ones. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years. "Call held" is `call_check_2y`, always the class's test (a tier row
counts the class calls on its dates): CHEAP should clear the hurdle or beat the benchmark (SPY), RICH should miss the hurdle and lag it.

**Hindsight the model could not see:**
- **The oil price collapse and the dividend cut.** Every two-year horizon of the 2014 dates, and the three-year horizon of the 2013 dates,
  runs through the commodity fall of late 2014 to early 2016 and Kinder Morgan's cut of its quarterly dividend to $0.125 (from $0.51),
  guided on 2015-12-08 and declared with the Q4 2015 release (2016-01-20).
  The stock went from $42.31 on 2014-12-31 to $14.54 a year later and $13.00 on 2016-01-15; no input of these models reads any of it.
- **The November 2014 combination.** KMI acquired KMP, KMR and EPB for shares and cash; the announcement (2014-08-10) is in the record from
  August 2014, but no input of the method reads it (it guides dividends, not revenue or EPS), and the combined company's first print falls
  after the range.

## 2013 (50 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 39 | +13.8% | -8.1% to +22.2% | 0 | 0 | +1.7% | 0 |
| class RICH, legacy tier BUY | 11 | -23.7% | -46.7% to +1.2% | 0 | 0 | +6.7% | 11 |
| EPS anchor $0.70 (2013-01-18 to 2013-02-22) | 6 | +20.8% | +18.4% to +22.2% | 0 | 0 | -1.9% | 0 |
| EPS anchor $0.56 (2013-03-01 to 2013-12-27) | 44 | +1.4% | -46.7% to +22.0% | 0 | 0 | +4.4% | 11 |
| latest print Q4 2012 (2013-01-18 to 2013-04-12) | 13 | +19.3% | +15.3% to +22.2% | 0 | 0 | -0.9% | 0 |
| latest print Q1 2013 (2013-04-19 to 2013-07-12) | 13 | +13.8% | +3.6% to +22.0% | 0 | 0 | +0.5% | 0 |
| latest print Q2 2013 (2013-07-19 to 2013-10-11) | 13 | -4.1% | -8.1% to +2.0% | 0 | 0 | +6.9% | 0 |
| latest print Q3 2013 (2013-10-18 to 2013-12-27) | 11 | -23.7% | -46.7% to +1.2% | 0 | 0 | +6.7% | 11 |

## 2014 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 51 | -37.8% | -53.2% to -30.3% | 0 | 0 | -37.3% | 0 |
| class RICH, legacy tier BUY | 2 | -48.4% | -48.7% to -48.4% | 0 | 0 | -3.0% | 2 |
| EPS anchor $0.56 (2014-01-03 to 2014-01-10) | 2 | -48.4% | -48.7% to -48.4% | 0 | 0 | -3.0% | 2 |
| EPS anchor $1.15 (2014-01-17 to 2014-12-31) | 51 | -37.8% | -53.2% to -30.3% | 0 | 0 | -37.3% | 0 |
| latest print Q3 2013 (2014-01-03 to 2014-01-10) | 2 | -48.4% | -48.7% to -48.4% | 0 | 0 | -3.0% | 2 |
| latest print Q4 2013 (2014-01-17 to 2014-04-11) | 13 | -37.3% | -53.2% to -30.3% | 0 | 0 | -5.2% | 0 |
| latest print Q1 2014 (2014-04-17 to 2014-07-11) | 13 | -38.4% | -43.3% to -36.3% | 0 | 0 | -25.8% | 0 |
| latest print Q2 2014 (2014-07-18 to 2014-10-10) | 13 | -36.1% | -42.0% to -33.4% | 0 | 0 | -47.2% | 0 |
| latest print Q3 2014 (2014-10-17 to 2014-12-31) | 12 | -40.9% | -45.3% to -37.6% | 0 | 0 | -52.2% | 0 |

## Across the series

| Group | Dates | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean m12-24 avg price | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class CHEAP | 90 | -17.4% | -38.8pp | -17.3% | -36.5% | 0 of 90 |
| class RICH | 13 | -28.7% | -47.1pp | +4.6% | -28.1% | 13 of 13 |

- **The CHEAP calls failed on every date.** None of the 90 CHEAP dates cleared the hurdle or beat SPY over two years (mean -17.4%,
  -38.8pp against SPY); the 13 RICH dates held all 13 (mean -28.7%). Every date's two-year price landed nearest its BEAR case, and the
  median drawdown within two years was -68.0%. Over one year the picture differs: CHEAP +0.4% on average, RICH +19.1%.
- **2013's CHEAP calls rested on revenue as reported.** BASE took the latest quarter's revenue growth, which the El Paso pipelines lifted
  to +27-65% through Q3 2013, less the share dilution; the 39 CHEAP dates of 2013 returned a median +13.8% over two years, none beating
  SPY. **The dividend-outlook BASE, scored in hindsight:** the sensitivity that put BASE on the dividend outlook's growth turned exactly
  those 39 dates RICH, and RICH would have held on all 39 (the GAAP-revenue CHEAP call on none). This is the sensitivity's own outcome and
  must not change the archive's rule: a rule change is a new method version, decided before scoring and tested out of sample, and this
  evidence is one stock in the year after an acquisition.
- **2014's CHEAP calls met the collapse.** On FY13's $1.15 the stock sat at 27-37x against a 33-35x median and at or near its BEAR case
  (Ratio B -0.01 to 0.04); the 51 CHEAP dates returned a median -37.8% over two years (-53.2% to -30.3%). BEAR (flat EPS at the 10th
  percentile P/E) was the right landing but far too mild: the BEAR price assumed the window's low multiple on unchanged EPS, while the
  price fell to roughly a third.
- **The readings ranked partly the right way.** Across the 103 m12-24 averages, the return to it ranks with the proxy composite at
  Spearman +0.45 (the right sign) and the EPP gap at -0.34 (the right sign: nearer the floor did better), but with Ratio B at +0.54 and
  the adjusted gap at +0.08 (the wrong signs) and the entry price at -0.27 (buying lower helped). The price was under the EPP floor on 6
  dates.
- **One stock, one acquisition and one crash.** The dates span the year after the El Paso acquisition, the drop-downs to KMP and EPB, and
  the months before and after the roll-up was announced; the outcomes are dominated by the 2015 commodity fall and the dividend cut. The
  result tests BASE on revenue as reported after an acquisition and the mildness of BEAR, not stock selection; it needs other midstream
  names on the same dates.

## 2015-2018 (210 dates)

The 210 weekly dates 2015-01-02 to 2018-12-31, built on 2026-11-16 after the 2013-2014 part above (the build 51b11d49e, README and firewall
result 235c9f40b), scored the same way. Every date has its 6-month, 1-, 2- and 3-year outcomes (the last two-year horizon ends 2020-12-30). The
same labels-only rule applies.

**Hindsight the model could not see:** the oil and gas price fall of 2015, the December 2015 dividend cut to $0.125 a quarter (from $0.51),
the stock's fall from about $44 (spring 2015) to $13 (January 2016), its range of about $15-23 in 2016-2019, and the COVID fall of 2020, which the
two-year horizons of the 2018 dates reach (2018-12-31 to 2020-12-30: +1.2%, -52.2pp against SPY).

### 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 40 | -37.3% | -48.7% to +27.8% | 0 | 0 | -38.3% | 0 |
| class FAIR, legacy tier BUY | 6 | -41.3% | -49.4% to -30.2% | 0 | 0 | -51.9% | 0 |
| class RICH, legacy tier BUY | 7 | -48.7% | -50.2% to -33.3% | 0 | 0 | -51.7% | 7 |
| EPS anchor $1.15 (2015-01-02 to 2015-01-16) | 3 | -42.4% | -45.9% to -40.2% | 0 | 0 | -53.9% | 0 |
| EPS anchor $0.89 (2015-01-23 to 2015-12-31) | 50 | -40.6% | -50.2% to +27.8% | 0 | 0 | -43.0% | 7 |
| latest print Q3 2014 (2015-01-02 to 2015-01-16) | 3 | -42.4% | -45.9% to -40.2% | 0 | 0 | -53.9% | 0 |
| latest print Q4 2014 (2015-01-23 to 2015-04-10) | 12 | -41.9% | -44.7% to -40.6% | 0 | 0 | -51.6% | 0 |
| latest print Q1 2015 (2015-04-17 to 2015-07-10) | 13 | -48.3% | -50.2% to -45.0% | 0 | 0 | -49.5% | 6 |
| latest print Q2 2015 (2015-07-17 to 2015-10-16) | 14 | -36.6% | -42.3% to -28.4% | 0 | 0 | -34.7% | 0 |
| latest print Q3 2015 (2015-10-23 to 2015-12-31) | 11 | -20.9% | -33.3% to +27.8% | 0 | 0 | -13.2% | 1 |

### 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | -7.8% | -20.5% to +57.8% | 3 | 1 | -4.3% | 3 |
| EPS anchor $0.89 (2016-01-08 to 2016-12-30) | 52 | -7.8% | -20.5% to +57.8% | 3 | 1 | -4.3% | 3 |
| latest print Q3 2015 (2016-01-08 to 2016-01-15) | 2 | +57.8% | +34.5% to +57.8% | 2 | 1 | +51.4% | 2 |
| latest print Q4 2015 (2016-01-22 to 2016-04-15) | 13 | -6.9% | -11.5% to +34.5% | 1 | 0 | +7.8% | 1 |
| latest print Q1 2016 (2016-04-22 to 2016-07-15) | 13 | -0.1% | -9.7% to +2.7% | 0 | 0 | +0.6% | 0 |
| latest print Q2 2016 (2016-07-22 to 2016-10-14) | 13 | -11.4% | -18.4% to -7.3% | 0 | 0 | -18.8% | 0 |
| latest print Q3 2016 (2016-10-21 to 2016-12-30) | 11 | -14.6% | -20.5% to -9.0% | 0 | 0 | -18.2% | 0 |

### 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +12.8% | -19.9% to +30.0% | 0 | 6 | -4.6% | 6 |
| EPS anchor $0.89 (2017-01-06 to 2017-12-29) | 52 | +12.8% | -19.9% to +30.0% | 0 | 6 | -4.6% | 6 |
| latest print Q3 2016 (2017-01-06 to 2017-01-13) | 2 | -18.2% | -19.9% to -18.2% | 0 | 0 | -21.7% | 0 |
| latest print Q4 2016 (2017-01-20 to 2017-04-13) | 13 | -2.9% | -15.3% to +0.2% | 0 | 0 | -20.0% | 0 |
| latest print Q1 2017 (2017-04-21 to 2017-07-14) | 13 | +12.8% | +2.1% to +21.4% | 0 | 0 | -5.2% | 0 |
| latest print Q2 2017 (2017-07-21 to 2017-10-13) | 13 | +14.7% | +6.0% to +16.9% | 0 | 0 | -1.7% | 0 |
| latest print Q3 2017 (2017-10-20 to 2017-12-29) | 11 | +22.8% | +17.1% to +30.0% | 0 | 6 | +9.8% | 6 |

### 2018 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +0.5% | -19.6% to +40.7% | 4 | 9 | +4.2% | 9 |
| EPS anchor $0.89 (2018-01-05 to 2018-12-31) | 53 | +0.5% | -19.6% to +40.7% | 4 | 9 | +4.2% | 9 |
| latest print Q3 2017 (2018-01-05 to 2018-01-12) | 2 | +20.7% | +18.8% to +20.7% | 0 | 0 | +5.4% | 0 |
| latest print Q4 2017 (2018-01-19 to 2018-04-13) | 13 | +21.2% | -14.5% to +40.7% | 4 | 9 | +23.8% | 9 |
| latest print Q1 2018 (2018-04-20 to 2018-07-13) | 13 | +4.2% | -10.4% to +17.7% | 0 | 0 | +13.4% | 0 |
| latest print Q2 2018 (2018-07-20 to 2018-10-12) | 13 | -10.3% | -19.6% to -7.5% | 0 | 0 | -0.8% | 0 |
| latest print Q3 2018 (2018-10-19 to 2018-12-31) | 12 | -0.0% | -18.6% to +2.7% | 0 | 0 | -3.1% | 0 |

### Across 2015-2018

| Group | Dates | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean m12-24 avg price | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class CHEAP | 197 | -4.7% | -31.1pp | -7.1% | -1.8% | 18 of 197 |
| class FAIR | 6 | -41.1% | -59.0pp | -47.5% | -48.8% | 0 of 6 |
| class RICH | 7 | -46.5% | -65.0pp | -48.9% | -54.0% | 7 of 7 |

- **Only the RICH calls held.** The 7 RICH dates of 2015 held all 7 (mean -46.5% over two years); the 6 FAIR dates of 2015 none; the 197
  CHEAP dates held 18 (mean -4.7%, -31.1pp against SPY). The two-year price landed nearest BASE on 120 dates and BEAR on 90, never BULL;
  the median drawdown within two years was -36.0%.
- **2015's calls were on FY14's $0.89 while the stock fell by two thirds.** The 2015 dates returned a median -40.8% over two years (-61.3pp
  against SPY); every class lost heavily (medians: CHEAP -37.3%, FAIR -41.3%, RICH -48.7%), so the RICH calls held only in the
  sense that nothing cleared the hurdle.
- **2016-2018's CHEAP calls rested on excluding the distorted years.** With FY15-FY17 out, FY14's $0.89 stayed the anchor and the stock sat
  at 15-29x, the bottom of its own range: CHEAP on every date. The returns were flat to modest (median two-year -7.8% for 2016, +12.8% for
  2017, +0.5% for 2018) and lagged SPY on 141 of the 157 (SPY beaten on 1, 6 and 9 dates). **The GAAP-kept
  variant, scored in hindsight:** keeping 2015-2017 at GAAP turned 155 of these CHEAP dates (2016-01-22 to 2018-12-31) RICH, and RICH would
  have held on 139 of them against 16 for the CHEAP call. This is that sensitivity's own outcome and must not change the archive's rule (a
  rule change is a new method version, decided before scoring and tested out of sample); it is one stock in one commodity cycle, and the
  GAAP anchors it reads ($0.01 for 2017) are themselves distortions.
- **The readings, on the m12-24 averages:** the entry price ranks at Spearman -0.94 and the EPP gap at -0.93 (buying lower and nearer the
  floor helped), Ratio B at -0.78 and the adjusted gap at +0.49 (the right signs), the proxy composite at -0.19 (the wrong sign). These
  mostly sort the high-priced early-2015 dates from the rest.
- **BEAR was too mild again in 2015,** as in 2014: flat-to-falling EPS at the 10th-percentile P/E, while the price fell to a third. From 2016
  the price sat under the EPP floor on most dates (168 of 210) and stayed there.

## 2019-2022 (209 dates)

The 209 weekly dates 2019-01-04 to 2022-12-30, built on 2026-11-16 after the 2015-2018 part above (the build ab586a2f6, README and firewall
result 99a564ef9, both pushed before any outcome was computed), scored the same way. Every date has its 6-month, 1-, 2- and 3-year outcomes (the
last two-year horizon ends 2024-12-30, the last three-year one 2025-12-30). The same labels-only rule applies.

**Hindsight the model could not see:** the COVID crash and the oil price collapse of March-April 2020 (the two-year windows of the 2019 dates
reach a low of $9.98 on 2020-03-18), Winter Storm Uri in February 2021 (a windfall the model first reads in the Q1 2021 release), the
2022 energy price surge, and the 2024 rerating of natural gas pipelines (a high of $28.54 on 2024-11-21 within the windows of the late-2022
dates).

### 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 11 | -6.9% | -13.4% to -2.2% | 0 | 0 | -19.2% | 0 |
| class CHEAP, legacy tier ACCUMULATE | 22 | -6.1% | -15.0% to +4.2% | 0 | 0 | -24.8% | 0 |
| class FAIR, legacy tier ACCUMULATE | 6 | -1.4% | -7.6% to +3.3% | 0 | 0 | -27.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 3 | -3.3% | -4.8% to -2.2% | 0 | 0 | -28.6% | 0 |
| class RICH, legacy tier ACCUMULATE | 7 | -7.2% | -10.7% to +2.7% | 0 | 0 | -18.1% | 7 |
| class RICH, legacy tier WATCHLIST | 3 | -14.9% | -17.3% to -6.5% | 0 | 0 | -20.7% | 3 |
| EPS anchor $0.89 (2019-01-04 to 2019-01-11) | 2 | -2.2% | -4.3% to -2.2% | 0 | 0 | -5.7% | 0 |
| EPS anchor $0.66 (2019-01-18 to 2019-12-27) | 50 | -6.1% | -17.3% to +4.2% | 0 | 0 | -23.9% | 10 |
| latest print Q3 2018 (2019-01-04 to 2019-01-11) | 2 | -2.2% | -4.3% to -2.2% | 0 | 0 | -5.7% | 0 |
| latest print Q4 2018 (2019-01-18 to 2019-04-12) | 13 | -7.4% | -13.4% to -2.8% | 0 | 0 | -26.8% | 0 |
| latest print Q1 2019 (2019-04-18 to 2019-07-12) | 13 | -1.4% | -6.3% to +4.2% | 0 | 0 | -27.2% | 0 |
| latest print Q2 2019 (2019-07-19 to 2019-10-11) | 13 | -6.1% | -15.0% to -2.0% | 0 | 0 | -23.4% | 0 |
| latest print Q3 2019 (2019-10-18 to 2019-12-27) | 11 | -7.6% | -17.3% to +2.7% | 0 | 0 | -19.3% | 10 |

### 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 50 | +41.1% | -15.4% to +77.2% | 38 | 29 | +21.7% | 40 |
| class RICH, legacy tier WATCHLIST | 3 | -9.1% | -12.9% to -6.4% | 0 | 0 | -21.4% | 3 |
| EPS anchor $0.66 (2020-01-03 to 2020-01-17) | 3 | -9.1% | -12.9% to -6.4% | 0 | 0 | -21.4% | 3 |
| EPS anchor $0.96 (2020-01-24 to 2020-12-31) | 50 | +41.1% | -15.4% to +77.2% | 38 | 29 | +21.7% | 40 |
| latest print Q3 2019 (2020-01-03 to 2020-01-17) | 3 | -9.1% | -12.9% to -6.4% | 0 | 0 | -21.4% | 3 |
| latest print Q4 2019 (2020-01-24 to 2020-04-17) | 13 | +8.5% | -15.4% to +59.2% | 6 | 0 | -11.0% | 6 |
| latest print Q1 2020 (2020-04-24 to 2020-07-17) | 13 | +36.6% | +17.2% to +45.6% | 8 | 5 | +15.5% | 10 |
| latest print Q2 2020 (2020-07-24 to 2020-10-16) | 13 | +50.5% | +37.1% to +59.7% | 13 | 13 | +30.1% | 13 |
| latest print Q3 2020 (2020-10-23 to 2020-12-31) | 11 | +46.9% | +33.1% to +77.2% | 11 | 11 | +30.0% | 11 |

### 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +16.2% | +0.0% to +46.1% | 8 | 44 | +6.9% | 44 |
| EPS anchor $0.96 (2021-01-08 to 2021-01-15) | 2 | +43.3% | +35.7% to +43.3% | 2 | 2 | +24.6% | 2 |
| EPS anchor $0.92 (2021-01-22 to 2021-04-16) | 13 | +25.0% | +13.0% to +46.1% | 6 | 13 | +14.5% | 13 |
| EPS anchor $1.237 (2021-04-23 to 2021-07-16) | 13 | +3.5% | +0.0% to +16.6% | 0 | 5 | -3.2% | 5 |
| EPS anchor $0.751 (2021-07-23 to 2021-10-15) | 13 | +15.2% | +4.7% to +23.3% | 0 | 13 | +3.5% | 13 |
| EPS anchor $0.75 (2021-10-22 to 2021-12-31) | 11 | +20.4% | +8.7% to +28.2% | 0 | 11 | +6.9% | 11 |
| latest print Q3 2020 (2021-01-08 to 2021-01-15) | 2 | +43.3% | +35.7% to +43.3% | 2 | 2 | +24.6% | 2 |
| latest print Q4 2020 (2021-01-22 to 2021-04-16) | 13 | +25.0% | +13.0% to +46.1% | 6 | 13 | +14.5% | 13 |
| latest print Q1 2021 (2021-04-23 to 2021-07-16) | 13 | +3.5% | +0.0% to +16.6% | 0 | 5 | -3.2% | 5 |
| latest print Q2 2021 (2021-07-23 to 2021-10-15) | 13 | +15.2% | +4.7% to +23.3% | 0 | 13 | +3.5% | 13 |
| latest print Q3 2021 (2021-10-22 to 2021-12-31) | 11 | +20.4% | +8.7% to +28.2% | 0 | 11 | +6.9% | 11 |

### 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 46 | +29.8% | +5.2% to +68.3% | 20 | 10 | +3.1% | 22 |
| class FAIR, legacy tier BUY | 3 | +14.2% | +8.1% to +16.1% | 0 | 0 | -8.6% | 0 |
| class RICH, legacy tier BUY | 3 | +9.2% | +6.9% to +15.9% | 0 | 0 | -12.2% | 3 |
| EPS anchor $0.75 (2022-01-07 to 2022-01-14) | 2 | +17.3% | +12.9% to +17.3% | 0 | 2 | -0.1% | 2 |
| EPS anchor $1.103 (2022-01-21 to 2022-07-15) | 26 | +12.8% | +5.2% to +36.6% | 3 | 0 | -4.9% | 6 |
| EPS anchor $1.159 (2022-07-22 to 2022-10-14) | 13 | +30.8% | +24.0% to +57.9% | 6 | 0 | +1.3% | 6 |
| EPS anchor $1.143 (2022-10-21 to 2022-12-30) | 11 | +61.7% | +47.3% to +68.3% | 11 | 8 | +8.5% | 11 |
| latest print Q3 2021 (2022-01-07 to 2022-01-14) | 2 | +17.3% | +12.9% to +17.3% | 0 | 2 | -0.1% | 2 |
| latest print Q4 2021 (2022-01-21 to 2022-04-14) | 13 | +10.7% | +5.2% to +16.6% | 0 | 0 | -2.3% | 0 |
| latest print Q1 2022 (2022-04-22 to 2022-07-15) | 13 | +15.9% | +6.9% to +36.6% | 3 | 0 | -7.5% | 6 |
| latest print Q2 2022 (2022-07-22 to 2022-10-14) | 13 | +30.8% | +24.0% to +57.9% | 6 | 0 | +1.3% | 6 |
| latest print Q3 2022 (2022-10-21 to 2022-12-30) | 11 | +61.7% | +47.3% to +68.3% | 11 | 8 | +8.5% | 11 |

### Across 2019-2022

| Group | Dates | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean m12-24 avg price | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class CHEAP | 181 | +22.4% | -5.9pp | +3.7% | +44.2% | 106 of 181 |
| class FAIR | 12 | +1.2% | -44.2pp | -22.3% | +17.6% | 0 of 12 |
| class RICH | 16 | -4.8% | -52.7pp | -18.0% | +14.8% | 16 of 16 |

- **The CHEAP calls of 2020-2022 held on 106 of 148; those of 2019 on none of 33.** On FY18's $0.66 the 2019 dates sat at 27-33x, near the
  window median; their two-year windows ran through the COVID crash (median drawdown -55.1%) and every 2019 date lagged SPY (median -54.4pp),
  so the 10 RICH calls of late 2019 held and the 33 CHEAP and 9 FAIR calls did not. From the Q4 2019 print FY19's $0.96 put the stock at
  12-23x, under the EPP floor, and the 2020 dates returned a median +40.7% over two years (38 of 53 cleared the hurdle). Across the series:
  CHEAP held 106 of 181 (mean +22.4% over two years, -5.9pp against SPY), FAIR none of 12 (+1.2%), RICH all 16 (-4.8%, -52.7pp).
- **Under the floor did better.** The price was under the EPP floor on 158 dates (median two-year return +26.4%) and above it on 51 (median
  -6.3%). On the m12-24 averages the entry price ranks at Spearman -0.94 and the EPP gap at -0.83 (buying lower and nearer the floor helped),
  Ratio B at -0.66 (the right sign), the adjusted gap at +0.11 and the proxy composite at -0.39 (the wrong signs). Over one year: CHEAP +9.2%
  on average, FAIR -18.1%, RICH -24.9%.
- **The earnings-guide encoding, scored in hindsight:** without it (the last full year's EPS standing, the 2013-2018 encoding) 10 dates of
  2022 change class (CHEAP or FAIR to RICH, 2022-04-22 to 2022-07-15), and the variant would have held 7 of them against 3 for the archive.
  **The largest sensitivity, scored the same way:** every signal at its BEAR value turns 57 dates (40 of 2019, 7 of early 2020, 10 of 2022) RICH or FAIR,
  and those calls would have held on 54 against 3; the adjusted-EPS variant (32 dates) on 7 against 16, the dividend-outlook BASE (28) and
  the signals at XBULL (28) on none against 16, FY2019 excluded on the KML gain alone (17) on none against 14, no buyback term (11) on none
  against 8, FY2020 at GAAP (6) on none against 3. These are the sensitivities' own outcomes and must not change the archive's rules (a rule
  change is a new method version, decided before scoring and tested out of sample): one stock, and the BEAR-signal result mostly reflects
  that the 2019 dates met the COVID crash.
- **Where the two-year price landed:** nearest BASE on 136 dates and BEAR on 73, never BULL; BEAR (2014's -22.6%/yr at the 10th-percentile
  P/E, $9-15) was close for the 2021 and 2022 dates (37 and 34 BEAR landings) whose prices rose, because BULL and BASE ran to $37-128 on the
  revenue-driven BASE of the Uri and 2022 quarters.
- **One stock through a crash and a commodity cycle.** The 2019 results are the COVID crash, the 2020-2022 results the recovery and the 2022
  energy surge; the series tests buying under the floor and the stock's own multiple history, not stock selection, and needs other midstream
  names on the same dates.

## 2023-2026 (202 dates)

The 202 weekly dates 2023-01-06 to 2026-11-13, built on 2026-11-16 after the 2019-2022 part above (the build 86f68447c, README and firewall
result 2f9f5e2f4, both pushed before any outcome was computed), scored the same way as far as the prices reach: the two-year horizon exists
for the 98 dates to 2024-11-15, the one-year horizon for the 150 dates to 2025-11-14, the six-month one for 176; the 26 dates from
2026-05-22 have none yet. The same labels-only rule applies, and the late dates' results will change as their horizons fill.

**Hindsight the model could not see:** the rerating of natural gas pipelines from 2024 on power demand (the stock went from a low of $16.03
on 2023-10-04 to a high of $34.43 on 2026-10-23 within these windows), and the earnings beats of 2025-2026 that the adjusted guides only
began to state in words.

### 2023 (52 dates; two-year outcomes)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +71.2% | +55.7% to +86.2% | 52 | 52 | +48.8% | 52 |
| EPS anchor $1.143 (2023-01-06 to 2023-01-13) | 2 | +63.4% | +62.0% to +63.4% | 2 | 2 | +13.6% | 2 |
| EPS anchor $1.12 (2023-01-20 to 2023-12-29) | 50 | +71.3% | +55.7% to +86.2% | 50 | 50 | +50.0% | 50 |
| latest print Q3 2022 (2023-01-06 to 2023-01-13) | 2 | +63.4% | +62.0% to +63.4% | 2 | 2 | +13.6% | 2 |
| latest print Q4 2022 (2023-01-20 to 2023-04-14) | 13 | +64.9% | +55.7% to +84.7% | 13 | 13 | +29.0% | 13 |
| latest print Q1 2023 (2023-04-21 to 2023-07-14) | 13 | +77.9% | +61.6% to +86.2% | 13 | 13 | +48.2% | 13 |
| latest print Q2 2023 (2023-07-21 to 2023-10-13) | 13 | +71.3% | +63.7% to +85.9% | 13 | 13 | +55.6% | 13 |
| latest print Q3 2023 (2023-10-20 to 2023-12-29) | 11 | +68.3% | +64.8% to +78.7% | 11 | 11 | +57.9% | 11 |

### 2024 to 2024-11-15 (46 dates; two-year outcomes)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 37 | +76.9% | +56.6% to +103.9% | 37 | 37 | +51.4% | 37 |
| class FAIR, legacy tier BUY | 1 | +56.9% | +56.9% to +56.9% | 1 | 1 | +39.7% | 0 |
| class RICH, legacy tier BUY | 1 | +51.9% | +51.9% to +51.9% | 1 | 1 | +40.0% | 0 |
| class RICH, legacy tier WATCHLIST | 1 | +41.5% | +41.5% to +41.5% | 1 | 1 | +29.4% | 0 |
| class RICH, legacy tier AVOID | 6 | +46.5% | +20.2% to +48.6% | 4 | 4 | +23.8% | 2 |
| EPS anchor $1.12 (2024-01-05 to 2024-01-12) | 2 | +67.7% | +62.7% to +67.7% | 2 | 2 | +52.2% | 2 |
| EPS anchor $1.22 (2024-01-19 to 2024-11-15) | 44 | +73.4% | +20.2% to +103.9% | 42 | 42 | +48.7% | 37 |
| latest print Q3 2023 (2024-01-05 to 2024-01-12) | 2 | +67.7% | +62.7% to +67.7% | 2 | 2 | +52.2% | 2 |
| latest print Q4 2023 (2024-01-19 to 2024-04-12) | 13 | +98.2% | +76.0% to +103.9% | 13 | 13 | +58.7% | 13 |
| latest print Q1 2024 (2024-04-19 to 2024-07-12) | 13 | +76.9% | +70.6% to +89.4% | 13 | 13 | +49.4% | 13 |
| latest print Q2 2024 (2024-07-19 to 2024-10-11) | 13 | +57.2% | +41.0% to +66.8% | 13 | 13 | +40.0% | 9 |
| latest print Q3 2024 (2024-10-18 to 2024-11-15) | 5 | +46.5% | +20.2% to +48.6% | 3 | 3 | +23.3% | 2 |

### 2024-11-22 to 2025-11-14 (52 dates; one-year outcomes only)

| Group | Dates | Median 1-yr total return | Range | Cleared 15% hurdle | Beat SPY | Class test held over one year |
|---|---|---|---|---|---|---|
| class FAIR, legacy tier ACCUMULATE | 11 | +24.3% | +17.3% to +37.7% | 11 | 10 | 9 |
| class FAIR, legacy tier WATCHLIST | 7 | +17.7% | +13.2% to +20.7% | 5 | 3 | 7 |
| class RICH, legacy tier ACCUMULATE | 2 | +35.0% | +32.9% to +35.0% | 2 | 2 | 0 |
| class RICH, legacy tier WATCHLIST | 17 | +22.6% | +15.0% to +28.4% | 17 | 5 | 0 |
| class RICH, legacy tier AVOID | 15 | +3.8% | -3.9% to +24.1% | 5 | 2 | 10 |
| EPS anchor $1.22 (2024-11-22 to 2025-01-17) | 9 | +2.1% | -3.9% to +4.3% | 0 | 0 | 9 |
| EPS anchor $1.26 (2025-01-24 to 2025-10-17) | 39 | +21.4% | +1.5% to +35.0% | 36 | 18 | 15 |
| EPS anchor $1.259 (2025-10-24 to 2025-11-14) | 4 | +33.8% | +17.3% to +37.7% | 4 | 4 | 2 |
| latest print Q3 2024 (2024-11-22 to 2025-01-17) | 9 | +2.1% | -3.9% to +4.3% | 0 | 0 | 9 |
| latest print Q4 2024 (2025-01-24 to 2025-04-11) | 12 | +27.1% | +1.5% to +35.0% | 11 | 9 | 1 |
| latest print Q1 2025 (2025-04-17 to 2025-07-11) | 13 | +19.6% | +15.0% to +25.5% | 13 | 0 | 0 |
| latest print Q2 2025 (2025-07-18 to 2025-10-17) | 14 | +20.5% | +13.2% to +29.2% | 12 | 9 | 14 |
| latest print Q3 2025 (2025-10-24 to 2025-11-14) | 4 | +33.8% | +17.3% to +37.7% | 4 | 4 | 2 |

### Across the dates with two-year outcomes

| Group | Dates | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean m12-24 avg price | Call held |
|---|---|---|---|---|---|
| class CHEAP | 89 | +74.8% | +30.1pp | +48.0% | 89 of 89 |
| class FAIR | 1 | +56.9% | +20.2pp | +39.7% | 0 of 1 |
| class RICH | 8 | +40.4% | +6.6pp | +24.9% | 2 of 8 |

- **The CHEAP calls of 2023 and 2024 held on all 89 dates with a two-year outcome** (mean +74.8% over two years, +30.1pp against SPY; every
  one cleared the hurdle and beat SPY). The price sat at 14-18x the year's guided EPS, under the EPP floor on 71 of these dates, and the
  two-year price landed nearest BULL on 83 of the 98 dates, the first part of the series where BULL was the usual landing.
- **The RICH calls came early.** From 2024-09-27 the stock traded at 20-25x against a window median near 20x and the class turned RICH;
  the 8 RICH dates with a two-year outcome returned +40.4% on average and held on 2 (the rerating continued). Over one year the 42 RICH
  dates to 2025-11-14 returned +16.1% (-4.1pp against SPY) and held on 15, the AVOID dates of November 2024 to January 2025 best (+2.1%
  median over one year, every one held); the 19 FAIR dates returned +22.7% over one year, the 89 CHEAP dates +37.8%.
- **The readings, on the m12-24 averages of the 98 two-year dates:** the entry price ranks at Spearman -0.57 and the EPP gap at -0.62 (buying
  lower and nearer the floor helped), Ratio B at -0.07 (the right sign, weak), the adjusted gap at -0.13 and the proxy composite at -0.16
  (the wrong signs).
- **The sensitivities, scored in hindsight, reverse the 2019-2022 reading:** every signal at its BEAR value turns 73 of the 98 two-year dates
  RICH or FAIR and those calls would have held on none (the archive's on 72), where in 2019-2022 the same variant would have held 54 of 57;
  the adjusted-EPS variant would have held 4 of its 53 changed dates against 52, no earnings guide 0 of 11 against 10. Over one year the
  XBULL-signal variant would have held all 40 of its changed dates against 15. One stock's sensitivities flip with the period, which is
  the reason they must not change the archive's rules (a rule change is a new method version, decided before scoring and tested out of
  sample).
- **One stock through a rerating.** The 2023-2024 results are a multiple expansion from the bottom of the stock's own range; the series tests
  buying near the floor and the stock's own multiple history, not stock selection, and the 2025-2026 calls are not scored yet over two years.
