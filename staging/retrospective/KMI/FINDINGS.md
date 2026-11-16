# KMI retrospective findings (hindsight)

Patterns seen in `outcome.json` for the KMI weekly dates: first the 103 of 2013-01-18 to 2014-12-31, then the 210 of 2015-2018 ("2015-2018",
below). The first part covers the 103 dates 2013-01-18 to 2014-12-31: Kinder Morgan, Inc. (NYSE: KMI, Class P common
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
