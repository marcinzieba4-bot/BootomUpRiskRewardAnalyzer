# CAT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CAT weekly dates: 105 from 2008-01-04 to 2009-12-31, all Caterpillar Inc. (NYSE: CAT). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time build
was committed and pushed (2008-2009: 26e9995). Outcomes were computed on 2026-11-11; every date has its 6-month, 1-, 2- and 3-year horizons
(the last ends 2012-12-31). Total returns include the quarterly dividends ($0.36, then $0.42 from July 2008, $0.44 from July 2010, $0.46
from July 2011 and $0.52 from July 2012, ex-dates); no split falls in any horizon, so every price is as traded. Medians of an even count take
the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the benchmark, and RICH should
miss the hurdle and lag the benchmark.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 36 | +14.0% | -21.6% to +152.0% | 14 | 32 | -7.9% | 32 |
| class CHEAP, legacy tier ACCUMULATE | 14 | -14.7% | -23.6% to -7.7% | 0 | 2 | -35.3% | 2 |
| class FAIR, legacy tier ACCUMULATE | 2 | -13.5% | -18.5% to -13.5% | 0 | 0 | -37.2% | 2 |
| class FAIR, legacy tier WATCHLIST | 1 | -18.1% | -18.1% to -18.1% | 0 | 0 | -41.3% | 1 |
| FY07E: guide midpoint $5.40 (2008-01-04 to 2008-01-18) | 3 | +1.0% | -9.8% to +2.1% | 0 | 3 | -35.8% | 3 |
| FY08E: $5.91, up 5-15% on FY07 (2008-01-25 to 2008-07-18) | 26 | -14.7% | -23.6% to -2.5% | 0 | 7 | -35.4% | 10 |
| FY08E: about $6.00 (2008-07-23 to 2008-12-31) | 24 | +110.4% | -2.1% to +152.0% | 14 | 24 | +54.5% | 24 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | +1.0% | -9.8% to +2.1% | 0 | 3 | -35.8% | 3 |
| latest print Q4 2007 (2008-01-25 to 2008-04-11) | 12 | -14.7% | -21.6% to -8.3% | 0 | 3 | -36.6% | 4 |
| latest print Q1 2008 (2008-04-18 to 2008-07-18) | 14 | -13.7% | -23.6% to -2.5% | 0 | 4 | -33.4% | 6 |
| latest print Q2 2008 (2008-07-23 to 2008-10-17) | 13 | +14.0% | -2.1% to +110.4% | 3 | 13 | -7.9% | 13 |
| latest print Q3 2008 (2008-10-22 to 2008-12-31) | 11 | +124.9% | +113.5% to +152.0% | 11 | 11 | +68.1% | 11 |

- **CHEAP held on 34 of 50 dates, and the entry month decided which.** The three January dates ($62.81-68.53, at 11.6-12.7x FY07's
  guided $5.40) returned -9.8% to +2.1% over two years and beat SPY (-16.3% to -10.2%). The 26 dates from the Q4 2007 print to
  2008-07-18 ($65.93-85.28, 11-14x the FY08 guide, 1-31% over the floor) returned -23.6% to -2.5% while SPY returned -18.7% to -6.8%:
  7 beat it, none cleared the hurdle, and the call held on 10 (the three FAIR dates among them, which landed within 15pp of SPY). The 24 dates from the Q2 2008 print ($34.67-72.42) returned -2.1% to +152.0% and all beat SPY; the 11 from 2008-10-22 (5.8-7.4x
  the $6.00 guide, 32-48% under the floor) returned +113.5% to +152.0% and all cleared the hurdle. Every 2008 date sat through a 53-74%
  drawdown; the low close was $22.17 on 2009-03-02. Over three years every 2008 date beat SPY (+21.0% to +177.8%, median +49.8%) and 24
  cleared the three-year hurdle.
- **The EPS anchor was right for 2008 and blind to 2009.** FY08 came in at $5.66 against the $5.91-6.00 the models carried (the Q4 2008
  release), so the 6-7x of October-December was on a real number; but the multiple a capital-goods maker earns at a peak year's EPS is not
  the multiple its history earned on average years, and the price was already discounting the 2009 fall (FY09: $1.43 reported, $2.18
  excluding redundancy costs, in the Q4 2009 release outside the series). Hypothesis, not a rule: a current-year P/E at a cyclical peak
  overstates cheapness; test on other cyclicals and periods, never fit it to CAT.
- **Ratio B and the adjusted gap ranked the dates, through the price.** Across the 53 dates the entry price ranks the two-year return at
  Spearman -0.87 and the return to the m12-24 average price at -0.82; the EPP gap at -0.89 and -0.85, Ratio B at -0.89 and -0.90 and the
  adjusted gap at +0.90 and +0.95 (all the right signs); the proxy composite at +0.70 and +0.77 (the right sign: 2.55-2.70 from Q1 2008
  to Q3 2008, 2.20 on Q4 2007). The two-year price landed nearest BASE on 35 dates and BEAR on 18 (0.51-0.87 times the BASE price, 1.8-3.4
  times BEAR).

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 13 | +262.5% | +124.8% to +358.3% | 13 | 13 | +152.1% | 13 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +209.6% | +209.6% to +209.6% | 1 | 1 | +121.7% | 1 |
| class FAIR, legacy tier ACCUMULATE | 1 | +209.5% | +209.5% to +209.5% | 1 | 1 | +118.8% | 0 |
| class RICH, legacy tier AVOID | 37 | +89.8% | +47.3% to +272.9% | 37 | 37 | +99.4% | 0 |
| FY08E: about $6.00 (2009-01-09 to 2009-01-23) | 3 | +145.2% | +124.8% to +169.7% | 3 | 3 | +78.2% | 3 |
| FY09E: $2.50 (2009-01-27 to 2009-04-17) | 12 | +270.7% | +209.5% to +358.3% | 12 | 12 | +159.7% | 11 |
| FY09E: about $1.25 (2009-04-22 to 2009-07-17) | 13 | +207.1% | +165.7% to +272.9% | 13 | 13 | +149.4% | 0 |
| FY09E: $1.15-2.25, midpoint $1.70 (2009-07-22 to 2009-10-16) | 13 | +80.2% | +47.3% to +181.0% | 13 | 13 | +96.5% | 0 |
| FY09E: $1.85-2.05, midpoint $1.95 (2009-10-21 to 2009-12-31) | 11 | +68.2% | +56.4% to +82.3% | 11 | 11 | +67.0% | 0 |

- **CHEAP held on all 14 dates to 2009-04-17** ($23.23-43.20): +124.8% to +358.3% over two years, all clearing the hurdle and beating SPY
  by 77-260pp. The one FAIR date (2009-02-06, $33.28) returned +209.5%, so its call missed.
- **RICH failed on all 37 dates from the Q1 2009 print.** At 23-32x the FY09 guide (the 93rd-100th percentile of the window) and 90-174%
  over the floor, the stock returned +47.3% to +272.9% over two years, cleared the hurdle and beat SPY on every date (by 35-215pp); over
  three years +51.0% to +248.3%. The two-year price landed nearest XBULL on all 37, at 6.7-12.8 times the BASE price and 1.7-3.5 times
  BULL. The call rested on two numbers that were trough numbers: EPS guided at $1.25-1.95 (the year's low multiple sets its own entry in
  the floor), and BASE growth taken from a sales guide down 25-39% and carried forward two years, which put the BASE price under the BEAR
  price. Hypothesis, not a rule: a current-year P/E at a cyclical trough, and a fiscal-year revenue guide extended as a two-year growth
  rate, read a recovery as richness; whether a normalized EPS or a one-year cap on a negative guide helps is a cross-ticker question for
  a new method version, never a CAT fit.
- **The price ranked the outcome; the composite did not.** Within 2009 the entry price ranks the two-year return at Spearman -0.95 and the
  m12-24 return at -0.93; the EPP gap at -0.76 and -0.67, Ratio B at -0.85 and -0.72, the adjusted gap at +0.77 and +0.63; the proxy
  composite, at its floor of 1.15 on every date from the Q1 2009 print (every signal at BEAR), at +0.09 and -0.13. The signals read the
  quarter that had just collapsed, not the recovery the price was already paying for.
- **Today's profile files CAT CYCLICAL** (`profile_drift` in every outcome), where the point-in-time rule read the 10-Ks' words as DURABLE;
  the kind changes the label only, so no price state above depends on it.
