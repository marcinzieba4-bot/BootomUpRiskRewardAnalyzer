# KMI retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 103 KMI weekly dates, 2013-01-18 to 2014-12-31: Kinder Morgan, Inc. (NYSE: KMI, Class P common
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
